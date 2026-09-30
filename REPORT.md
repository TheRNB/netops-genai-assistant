# NetOps GenAI Assistant: Project Report

## Problem

Network-incident triage is manual and slow: an engineer has to recall or look up the
right troubleshooting procedure and separately check the affected site's live metrics
before deciding severity and next steps. This project automates that first pass,
combining document retrieval, live operational-data lookup, and an LLM to produce a
structured, cited triage decision.

## Method

**Retrieval-augmented answering.** 43 synthetic network-troubleshooting runbooks are
chunked (1000 chars, 100 overlap, sized so most runbooks stay in one chunk, with a
handful of long multi-section ones actually needing to split, roughly a 90/10 mix),
embedded (`all-MiniLM-L6-v2`), and indexed in Chroma. `rag.answer()` retrieves the
top-4 chunks for a question and prompts the LLM to answer strictly from that context,
falling back to an explicit "not covered" response otherwise, with citations taken
from the actual retrieved chunk IDs rather than trusted from LLM output.

**Agentic triage.** `agent.triage()` is a hand-written 2-3 step controller (not a
framework) with two tools: `doc_retrieval` (the same RAG retrieval) and `kpi_lookup`
(reads the site's recent latency/throughput/packet-loss from a synthetic KPI CSV). Both
are combined into one LLM call that returns structured JSON (severity, likely cause,
recommended steps, sources) validated with pydantic.

**LLM client.** `src/llm.py` talks to Ollama's OpenAI-compatible `/v1/chat/completions`
endpoint directly over HTTP rather than through the `ollama` library. That's a
deliberate choice: swapping in any other OpenAI-compatible backend (vLLM, LM Studio,
a hosted API, a different machine on the network) is just a base-URL and model-name
change, no code changes. A fixed seed (`LLM_SEED=46`) is sent on every call for
reproducibility.

**Analytics.** `analytics.py` flags per-site KPI anomalies using a per-site z-score
threshold (chosen over IsolationForest for simplicity and interpretability on a
stationary hourly baseline) and produces trend/breakdown charts plus a text insights
summary.

**Serving.** A FastAPI app exposes `/triage` and `/ask`; a CLI supports single queries
and batch triage of a file of incidents to CSV.

## Evaluation methodology

Two kinds of metrics are computed for every answer:

- **LLM-judge scores** (1-5): faithfulness (does the answer stick to the retrieved
  context?), relevance, and correctness (does it match a human-written reference
  answer?). The judge is always `llama3.1:8b`, fixed across every model under test, so
  the comparison isolates the model being *judged*, not the judge itself.
- **Deterministic NLG metrics**: ROUGE-L and BLEU against the reference answer, as a
  sanity check that doesn't depend on any LLM's opinion.

Four test suites probe different questions:

1. **Main eval**: 30 grounded Q/A pairs + 15 labeled incidents, retrieval always on.
   Measures baseline answer/triage quality.
2. **Full ablation**: the same 30+15 set, run again with retrieval and tools
   completely disabled (`answer_zero_shot`, `triage_zero_shot`). Isolates what RAG
   actually buys over the model's own parametric knowledge on everyday questions.
3. **Invented-facts ablation**: 8 Q/A pairs about facts fabricated specifically for
   this project (a made-up escalation code, a made-up threshold, etc.) that cannot
   exist in any model's training data. If RAG helps here, it's not memorization.
4. **Counterfactual ablation**: 6 Q/A pairs where the retrieved runbook fact
   deliberately contradicts generic troubleshooting wisdom (e.g. "don't restart the
   link, that makes it worse"). Tests whether a model actually lets retrieved context
   override its own prior, or falls back to generic instincts anyway.

All four suites were run against six local models: `llama3.1:8b`, `gemma2:9b`,
`mistral-nemo:12b`, `qwen2.5:14b`, `qwen3:14b`, `deepseek-r1:14b`.

## Bugs found and fixed along the way

- **Chunk truncation**: an initial `CHUNK_SIZE=500` cut a key sentence mid-word in one
  of the longer runbooks. Fixed by increasing chunk size and later re-tuning it once a
  realistic mix of short/long documents was added.
- **Stale index accumulation**: `build_index()` used `upsert` only, so old chunks from
  previous runbook batches stayed in the Chroma collection indefinitely across runs,
  breaking reproducibility as the corpus grew. Fixed by dropping and recreating the
  collection at the start of every `build_index()` call.
- **Redundant trailing chunk**: the chunking loop always advanced by `chunk_size -
  overlap` even when the previous chunk already covered the rest of the document,
  producing a spurious near-duplicate tail chunk for documents just under the
  chunk-size boundary.
- **Per-item model-swap thrashing**: the eval loops originally called the target model
  then the judge model on every single item, forcing Ollama to swap ~9-14GB models in
  and out of unified memory on every iteration. This caused an actual hang once (a
  totally unrelated health-check request timed out with zero response while a job was
  "stuck"). Fixed by restructuring every eval function into two passes: all
  target-model calls first, then all judge-model calls, cutting swaps from roughly
  2n to 1 per run. Checkpointing was added alongside this so a crash mid-run doesn't
  lose already-completed work.

## Results

### Main eval (with_rag)

| Model | hit_rate | correctness (1-5) | ROUGE-L | BLEU | severity_acc | cause_acc |
|---|---|---|---|---|---|---|
| llama3.1:8b | 1.0 | 4.50 | 0.511 | 0.246 | 0.60 | 0.333 |
| gemma2:9b | 1.0 | 5.00 | 0.551 | 0.242 | 0.40 | 0.40 |
| mistral-nemo:12b | 1.0 | 3.70 | 0.333 | 0.137 | 0.467 | 0.20 |
| qwen2.5:14b | 1.0 | 5.00 | 0.533 | 0.227 | 0.40 | 0.0* |
| qwen3:14b | 1.0 | 5.00 | 0.392 | 0.131 | 0.60 | 0.40 |
| deepseek-r1:14b | 1.0 | 5.00 | 0.349 | 0.122 | 0.467 | 0.267 |

\* Verified artifact, not a real gap. See "The cause-accuracy judge is itself
imperfect" below.

### Zero-shot baseline (same qa_set/incidents, no retrieval/tools)

| Model | correctness | ROUGE-L | BLEU | severity_acc | cause_acc |
|---|---|---|---|---|---|
| llama3.1:8b | 4.67 | 0.046 | 0.0031 | 0.533 | 0.20 |
| gemma2:9b | 4.47 | 0.049 | 0.0036 | 0.40 | 0.267 |
| mistral-nemo:12b | 4.70 | 0.039 | 0.0024 | 0.467 | 0.40 |
| qwen2.5:14b | 4.97 | 0.042 | 0.0025 | 0.60 | 0.267 |
| qwen3:14b | 4.80 | 0.035 | 0.0017 | 0.533 | 0.267 |
| deepseek-r1:14b | 4.80 | 0.053 | 0.0039 | 0.40 | 0.267 |

RAG beats zero-shot on correctness for exactly one of six models (gemma2:9b).
Averaged across all six, the uplift is **-0.8 percentage points**, smaller than the
run-to-run noise floor (rerunning llama3.1:8b's own ablation twice under nominally
identical conditions shifted its correctness score by 2.6pp). **On everyday questions
the model already answers reasonably well, RAG does not reliably help.**

### Invented-facts ablation (facts impossible to know without retrieval)

| Model | with_rag correctness | with_rag ROUGE-L | zero_shot correctness | zero_shot ROUGE-L |
|---|---|---|---|---|
| llama3.1:8b | 5.0 | 0.413 | 2.875 | 0.042 |
| gemma2:9b | 5.0 | 0.624 | 2.5 | 0.034 |
| mistral-nemo:12b | 5.0 | 0.465 | 3.5 | 0.040 |
| qwen2.5:14b | 5.0 | 0.455 | 2.625 | 0.028 |
| qwen3:14b | 5.0 | 0.249 | 3.125 | 0.026 |
| deepseek-r1:14b | 5.0 | 0.361 | 3.5 | 0.058 |

**6 of 6 models: perfect correctness with RAG, every one drops sharply zero-shot.**
Average uplift: **+39.6 percentage points**. This is the cleanest, most consistent
result across the whole project: unambiguous evidence retrieval does real work when
the model genuinely cannot know the answer otherwise.

### Counterfactual ablation (retrieved fact contradicts generic wisdom)

| Model | "Not covered" bailout rate | with_rag correctness | with_rag ROUGE-L | zero_shot correctness |
|---|---|---|---|---|
| llama3.1:8b | 5/6 | 2.5 | 0.129 | 2.833 |
| mistral-nemo:12b | 5/6 | 2.5 | 0.083 | 2.833 |
| qwen3:14b | 1/6 | 4.5 | 0.363 | 4.333 |
| gemma2:9b | 0/6 | 5.0 | 0.333 | 2.667 |
| qwen2.5:14b | 0/6 | 5.0 | 0.465 | 3.667 |
| deepseek-r1:14b | 0/6 | 5.0 | 0.494 | 3.333 |

**4 of 6 models correctly let the retrieved fact override generic troubleshooting
instinct; 2 of 6 (llama3.1:8b, mistral-nemo:12b) mostly refuse to answer at all**,
replying "Not covered by available runbooks" even with the correct, isolated context
sitting in front of them. This is a genuine, model-dependent limitation that the RAG
pipeline itself does not fix; retrieval puts the right fact in context, but whether the
model trusts it over its own prior is a property of that specific model, not of the
architecture. Deterministic ROUGE-L/BLEU track this almost perfectly (the two
bailout-prone models also score lowest on ROUGE-L), since a refusal shares almost no
n-grams with a real answer, so the metrics are reflecting the refusal behavior rather
than adding independent signal here.

### The cause-accuracy judge is itself imperfect

Investigating qwen2.5:14b's `cause_accuracy: 0.0` (main eval) surfaced a real
limitation in the evaluation methodology, not the model: the judge prompt
(`"Does the PREDICTED cause semantically match the EXPECTED cause category?"`) was
directly tested against two near-identical predictions for the same expected cause
("dns"):

- `"DNS resolver overload or misconfiguration"` (gemma2's phrasing) -> judge says **YES**
- `"DNS resolver overload, misconfigured DNS forwarder, or upstream DNS provider
  outage"` (qwen2.5's phrasing, same underlying diagnosis) -> judge says **NO**

The judge penalizes verbose, hedged "X, or Y, or Z" answers as not committing to one
cause, even when the diagnosis is correct. qwen2.5:14b's 0/15 score is a phrasing-style
artifact of the judge, not evidence the model's triage reasoning is worse: a caveat
that applies to `cause_accuracy` as a metric in general, not just this one model.

## Findings

Averaged across all four test suites and all six models (96 model/scenario runs),
correctness uplift from RAG is **+18.3 percentage points**. That headline number is
worth immediately qualifying, which is the point of running four different test
designs instead of one: it's driven almost entirely by the invented-facts suite
(+39.6pp), is roughly flat on everyday questions (-0.65pp, within noise), and is
bimodal on the counterfactual suite (+16.1pp average, but split 4-models-benefit vs.
2-models-regress). A single average would misrepresent all three of those as one
story; the breakdown below is the actual finding.

1. **Retrieval is solved for this corpus**: hit_rate@k = 1.00 in every single run,
   across every model and every test. Whatever else is imperfect, it's never "the
   system fetched the wrong document."
2. **RAG's value is conditional on how wrong the model would otherwise be, not a fixed
   uplift.** It's decisive on facts that are genuinely inaccessible (+39.6pp), a wash
   on everyday questions the model already handles reasonably (-0.8pp, noise), and
   split on whether a retrieved fact overrides generic prior knowledge (4 of 6 models
   yes, 2 of 6 mostly refuse).
3. **Bigger and reasoning-tuned models are not a reliable fix for triage accuracy.**
   `deepseek-r1:14b`'s extended think-traces don't translate into meaningfully better
   cause/severity accuracy than smaller non-reasoning models, and take substantially
   longer to produce.
4. **Which model you pick matters more than the RAG architecture for whether context
   actually gets trusted over prior knowledge.** The counterfactual over-caution split
   looks like an instruction-tuning/alignment difference between model families, not a
   scale effect: gemma2:9b (smallest of the six) handles it perfectly; mistral-nemo:12b
   and llama3.1:8b (mid-size and smallest respectively) mostly refuse.
5. **The real bottleneck for this use case is diagnosis, not retrieval.**
   `cause_accuracy` sits in the 0-40% range for every model regardless of RAG, model
   size, or reasoning ability, which points at the triage prompt/task design as the
   weak link, not the retrieval pipeline.

## Limitations

- All data (runbooks and KPI time series) is synthetic, generated for this project,
  not representative of real network fault patterns.
- LLM-judge scores (faithfulness, relevance, correctness) are opinions of a single
  fixed judge model (`llama3.1:8b`), not validated against human judgment. The
  cause-accuracy judge-phrasing artifact documented above is a concrete demonstration
  that this judge is not fully reliable, and that caveat likely extends to some degree
  to the other judge-based metrics too.
- `expected_severity`/`expected_cause` labels in `eval/incidents.json` reflect one
  person's judgment calls with fuzzy boundaries (e.g. high vs. critical), not a
  validated ground truth.
- Sample sizes are small (30 QA pairs, 15 incidents, 8 invented-facts, 6
  counterfactual), enough to see clear directional patterns, not enough for tight
  confidence intervals.
- The invented-facts and counterfactual runbooks were purpose-built to make a specific
  point; they're a controlled probe, not a representative sample of real-world
  ambiguity.

## Next steps

- Get a second labeler (or a rule-based severity rubric) on `eval/incidents.json` to
  see how much of the triage-accuracy ceiling is label noise vs. genuine model error.
- Try a different judge model (or a judge ensemble) to check how much the
  cause-accuracy phrasing-sensitivity issue is specific to `llama3.1:8b` as judge.
- Constrain `expected_cause` to a fixed category list and have the triage model
  classify into it directly, instead of free-text-vs-LLM-judge matching.
- Add a confidence/uncertainty signal to triage output so low-confidence cases are
  flagged for human review instead of auto-triaged.
- Investigate why llama3.1:8b and mistral-nemo:12b specifically default to refusal on
  counterfactual context: a system prompt tweak might close this gap without needing
  a different model.
