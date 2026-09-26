# NetOps GenAI Assistant — Project Report

## Problem

Network-incident triage is manual and slow: an engineer has to recall or look up the
right troubleshooting procedure and separately check the affected site's live metrics
before deciding severity and next steps. This project automates that first pass —
combining document retrieval, live operational-data lookup, and an LLM to produce a
structured, cited triage decision.

## Method

**Retrieval-augmented answering.** 25 synthetic network-troubleshooting runbooks are
chunked, embedded (`all-MiniLM-L6-v2`), and indexed in Chroma. `rag.answer()` retrieves
the top-k chunks for a question and prompts the LLM to answer strictly from that
context, falling back to an explicit "not covered" response otherwise, with citations
taken from the actual retrieved chunk IDs rather than trusted from LLM output.

**Agentic triage.** `agent.triage()` is a hand-written 2-3 step controller (not a
framework) with two tools: `doc_retrieval` (the same RAG retrieval) and `kpi_lookup`
(reads the site's recent latency/throughput/packet-loss from a synthetic KPI CSV). Both
are combined into one LLM call that returns structured JSON (severity, likely cause,
recommended steps, sources) validated with pydantic.

**Analytics.** `analytics.py` flags per-site KPI anomalies using a per-site z-score
threshold (chosen over IsolationForest for simplicity and interpretability on a
stationary hourly baseline) and produces trend/breakdown charts plus a text insights
summary.

**Serving.** A FastAPI app exposes `/triage` and `/ask`; a CLI supports single queries
and batch triage of a file of incidents to CSV.

## Evaluation

30 grounded Q/A pairs (question, reference answer, gold source doc) and 15 labeled
incidents (expected cause, expected severity) were built from the runbook corpus.

- **RAG retrieval**: hit-rate@k = 1.00 (gold doc always in the top-4 retrieved chunks).
- **RAG answer quality**: LLM-judged faithfulness 4.73/5, relevance 4.93/5.
- **Triage severity accuracy**: 0.60 (9/15 exact matches against the labeled severity).
- **Triage cause accuracy**: 0.47 (7/15, judged by semantic match against the expected
  cause category).

`ragas` was the originally planned RAG evaluation library but its pinned version
(0.2.10) fails to import against the installed `langchain-community` version (a removed
`ChatVertexAI` symbol), so a direct LLM-as-judge prompt was used instead — a pragmatic
substitution rather than a blocker.

## LLM backend comparison

The initial hypothesis was that the local 8B model's reasoning ceiling was the main
cause of the triage-accuracy gap. To test that, the same eval suite (fixed judge model
throughout) was run against 6 local backends spanning size and vendor — llama3.1:8b,
deepseek-r1:8b/14b (reasoning-tuned), qwen2.5:14b, mistral-nemo:12b, gemma2:9b. Full
numbers are in the README and `eval/model_comparison.json`.

The hypothesis didn't hold. RAG faithfulness/relevance stayed within a tight band
(4.6-5.0) regardless of model, and triage severity/cause accuracy did not improve with
size or reasoning-tuning — `deepseek-r1:14b` matched the best scores achieved by the
5-minute `llama3.1:8b` baseline, but took 37 minutes (7x) to do it, and `qwen2.5:14b`
scored no better than the smaller `gemma2:9b`. Bigger/slower is not obviously better
here.

## Findings

Retrieval is essentially solved for this corpus: 25 runbooks covering distinct,
non-overlapping failure modes make top-k retrieval trivial, and grounded answers score
well across every model tested. Triage is meaningfully harder, but the backend
comparison shows model size/capability is not the bottleneck — the gap more likely
comes from the eval methodology itself: `expected_severity` labels were my own judgment
calls with fuzzy boundaries (e.g. high vs. critical), and cause-accuracy is judged by
one LLM guessing whether another LLM's free-text explanation "matches" a short category
label, which stacks two sources of judgment noise on top of the underlying task. That
the accuracy ceiling is roughly the same across six different models, including
reasoning-tuned ones, is itself evidence for that reading. This gap is the most
interesting/legitimate finding of the project, not a bug to hide.

## Limitations

- All data (runbooks and KPI time series) is synthetic, generated for this project —
  not representative of real network fault patterns.
- The runbook corpus (25 docs) is small and topically non-overlapping, which makes the
  retrieval metric close to trivial — a larger, messier corpus would be a more honest
  retrieval benchmark.
- Triage cause-accuracy is judged by LLM semantic matching against a short category
  label, which is itself an approximate metric, and `expected_severity`/`expected_cause`
  labels in `eval/incidents.json` reflect one person's judgment calls, not a validated
  ground truth.
- The backend comparison used the same eval methodology throughout, so it rules out
  "the model is too small" but can't rule out "the eval set/metric itself is the
  ceiling" — that would need a cleaner ground truth to test.

## Next steps

- Get a second labeler (or a rule-based severity rubric) on `eval/incidents.json` to see
  how much of the triage-accuracy ceiling is label noise vs. genuine model error.
- Constrain `expected_cause` to a fixed category list and have the triage model classify
  into it directly, instead of free-text-vs-LLM-judge matching.
- Add a confidence/uncertainty signal to triage output so low-confidence cases are
  flagged for human review instead of auto-triaged.
- Grow the runbook corpus with overlapping/ambiguous cases to make retrieval a
  meaningful discriminator again.
