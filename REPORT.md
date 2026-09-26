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

## Findings

Retrieval is essentially solved for this corpus: 25 runbooks covering distinct,
non-overlapping failure modes make top-k retrieval trivial, and grounded answers score
well. Triage is meaningfully harder — severity and cause judgments require reasoning
over combined runbook + KPI context, and the local 8B model's judgment doesn't match the
labeled ground truth as reliably as its RAG-answering ability does. This gap is the
most interesting/legitimate finding of the project, not a bug to hide.

## Limitations

- All data (runbooks and KPI time series) is synthetic, generated for this project —
  not representative of real network fault patterns.
- The local 8B Ollama model has a lower reasoning ceiling than larger hosted models,
  which plausibly explains most of the triage-accuracy gap.
- The runbook corpus (25 docs) is small and topically non-overlapping, which makes the
  retrieval metric close to trivial — a larger, messier corpus would be a more honest
  retrieval benchmark.
- Triage cause-accuracy is judged by LLM semantic matching against a short category
  label, which is itself an approximate metric.

## Next steps

- Expand the incident/label set and add inter-rater or rule-based validation to make
  triage accuracy a sturdier metric.
- Try a larger or fine-tuned model specifically on the triage-decision task and compare
  against the current baseline.
- Add a confidence/uncertainty signal to triage output so low-confidence cases are
  flagged for human review instead of auto-triaged.
- Grow the runbook corpus with overlapping/ambiguous cases to make retrieval a
  meaningful discriminator again.
