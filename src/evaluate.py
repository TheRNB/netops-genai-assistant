import json
import re

import sacrebleu
from rouge_score import rouge_scorer
from tqdm import tqdm

from src.agent import triage, triage_zero_shot
from src.config import EVAL_DIR
from src.llm import generate
from src.rag import answer, answer_zero_shot, retrieve

_rouge = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
_CHECKPOINT_DIR = EVAL_DIR / "checkpoints"


# Ollama can only keep one big model loaded at a time, so if we called the target model and the
# judge model back-to-back inside one loop it'd swap models on every single item. Writing this so
# every function does all its target-model calls first, then all its judge-model calls, keeps each
# model loaded for one long stretch instead of thrashing. Also dumps progress here so a crash
# partway through doesn't lose whatever's already been computed.
def _checkpoint(name: str, model: str | None, data) -> None:
    _CHECKPOINT_DIR.mkdir(exist_ok=True)
    safe_model = (model or "default").replace(":", "_").replace("/", "_")
    (_CHECKPOINT_DIR / f"{name}_{safe_model}.json").write_text(json.dumps(data, indent=2))


# Deterministic, no LLM call — a fast sanity check alongside the LLM-judge scores above.
def _rouge_l(reference: str, answer_text: str) -> float:
    return _rouge.score(reference, answer_text)["rougeL"].fmeasure


def _bleu(reference: str, answer_text: str) -> float:
    return sacrebleu.sentence_bleu(answer_text, [reference]).score / 100

# ragas 0.2.10 won't import here (missing ChatVertexAI), so we just prompt the LLM to judge directly.
_JUDGE_PROMPT = (
    "Rate the ANSWER on a 1-5 scale for {aspect} given the QUESTION and CONTEXT. "
    "Reply with ONLY the integer.\n\nQUESTION: {question}\nCONTEXT: {context}\nANSWER: {answer}"
)

# Same idea but scored against a reference answer instead of retrieved context — works with or without RAG.
_CORRECTNESS_PROMPT = (
    "Rate how well the ANSWER matches the REFERENCE ANSWER on a 1-5 scale (5 = same facts, 1 = contradicts or "
    "unrelated). Reply with ONLY the integer.\n\nQUESTION: {question}\nREFERENCE ANSWER: {reference}\nANSWER: {answer}"
)

# Fixed so every model is graded by the same judge.
JUDGE_MODEL = "llama3.1:8b"


def _judge_score(question: str, context: str, answer_text: str, aspect: str) -> int:
    prompt = _JUDGE_PROMPT.format(aspect=aspect, question=question, context=context, answer=answer_text)
    reply = generate(prompt, model=JUDGE_MODEL)
    match = re.search(r"[1-5]", reply)
    return int(match.group()) if match else 1


def _correctness_score(question: str, reference: str, answer_text: str) -> int:
    prompt = _CORRECTNESS_PROMPT.format(question=question, reference=reference, answer=answer_text)
    reply = generate(prompt, model=JUDGE_MODEL)
    match = re.search(r"[1-5]", reply)
    return int(match.group()) if match else 1


def hit_rate_at_k(qa_set: list[dict], k: int = 4) -> float:
    hits = 0
    for item in qa_set:
        retrieved_ids = {h["source_doc_id"] for h in retrieve(item["question"], k=k)}
        if item["gold_doc_id"] in retrieved_ids:
            hits += 1
    return hits / len(qa_set) if qa_set else 0.0


def evaluate_rag(qa_set: list[dict], model: str | None = None) -> dict:
    # Pass 1: generation, all on the target model — no swapping to the judge model yet.
    generated = []
    for item in tqdm(qa_set, desc="evaluate_rag: generate"):
        result = answer(item["question"], model=model)
        context = "\n".join(h["text"] for h in retrieve(item["question"]))
        generated.append({**item, "context": context, "model_answer": result["answer"]})
    _checkpoint("evaluate_rag_generated", model, generated)

    # Pass 2: judging, all on the fixed judge model — one swap total instead of one per item.
    faithfulness_scores, relevance_scores, correctness_scores = [], [], []
    rouge_l_scores, bleu_scores = [], []
    for item in tqdm(generated, desc="evaluate_rag: judge"):
        ans = item["model_answer"]
        faithfulness_scores.append(_judge_score(item["question"], item["context"], ans, "faithfulness to the context"))
        relevance_scores.append(_judge_score(item["question"], item["context"], ans, "relevance to the question"))
        correctness_scores.append(_correctness_score(item["question"], item["reference_answer"], ans))
        rouge_l_scores.append(_rouge_l(item["reference_answer"], ans))
        bleu_scores.append(_bleu(item["reference_answer"], ans))

    return {
        "hit_rate_at_k": hit_rate_at_k(qa_set),
        "avg_faithfulness": sum(faithfulness_scores) / len(faithfulness_scores),
        "avg_relevance": sum(relevance_scores) / len(relevance_scores),
        "avg_correctness": sum(correctness_scores) / len(correctness_scores),
        "avg_rouge_l": sum(rouge_l_scores) / len(rouge_l_scores),
        "avg_bleu": sum(bleu_scores) / len(bleu_scores),
        "n": len(qa_set),
    }


# Ablation baseline: same qa_set, no retrieval at all, scored only on correctness (no context to judge faithfulness against).
def evaluate_rag_zero_shot(qa_set: list[dict], model: str | None = None) -> dict:
    generated = []
    for item in tqdm(qa_set, desc="evaluate_rag_zero_shot: generate"):
        result = answer_zero_shot(item["question"], model=model)
        generated.append({**item, "model_answer": result["answer"]})
    _checkpoint("evaluate_rag_zero_shot_generated", model, generated)

    correctness_scores, rouge_l_scores, bleu_scores = [], [], []
    for item in tqdm(generated, desc="evaluate_rag_zero_shot: judge"):
        ans = item["model_answer"]
        correctness_scores.append(_correctness_score(item["question"], item["reference_answer"], ans))
        rouge_l_scores.append(_rouge_l(item["reference_answer"], ans))
        bleu_scores.append(_bleu(item["reference_answer"], ans))
    return {
        "avg_correctness": sum(correctness_scores) / len(correctness_scores),
        "avg_rouge_l": sum(rouge_l_scores) / len(rouge_l_scores),
        "avg_bleu": sum(bleu_scores) / len(bleu_scores),
        "n": len(qa_set),
    }


# Cause labels are free text vs. a short category, so match them by LLM judgment rather than exact string equality.
def _cause_matches(expected_cause: str, likely_cause: str) -> bool:
    prompt = (
        "Does the PREDICTED cause semantically match the EXPECTED cause category? Reply with ONLY YES or NO.\n\n"
        f"EXPECTED: {expected_cause}\nPREDICTED: {likely_cause}"
    )
    return "yes" in generate(prompt, model=JUDGE_MODEL).lower()


def triage_accuracy(incidents: list[dict], model: str | None = None) -> dict:
    # Pass 1: triage calls on the target model.
    triaged = []
    for item in tqdm(incidents, desc="triage_accuracy: triage"):
        result = triage(item["incident_text"], model=model)
        triaged.append({**item, "severity": result.severity, "likely_cause": result.likely_cause})
    _checkpoint("triage_accuracy_triaged", model, triaged)

    # Pass 2: cause-matching on the fixed judge model.
    severity_correct, cause_correct = 0, 0
    for item in tqdm(triaged, desc="triage_accuracy: judge"):
        severity_correct += item["severity"] == item["expected_severity"]
        cause_correct += _cause_matches(item["expected_cause"], item["likely_cause"])
    n = len(incidents)
    return {
        "severity_accuracy": severity_correct / n if n else 0.0,
        "cause_accuracy": cause_correct / n if n else 0.0,
        "n": n,
    }


# Ablation baseline: same incidents, no doc_retrieval/kpi_lookup tools at all.
def triage_accuracy_zero_shot(incidents: list[dict], model: str | None = None) -> dict:
    triaged = []
    for item in tqdm(incidents, desc="triage_accuracy_zero_shot: triage"):
        result = triage_zero_shot(item["incident_text"], model=model)
        triaged.append({**item, "severity": result.severity, "likely_cause": result.likely_cause})
    _checkpoint("triage_accuracy_zero_shot_triaged", model, triaged)

    severity_correct, cause_correct = 0, 0
    for item in tqdm(triaged, desc="triage_accuracy_zero_shot: judge"):
        severity_correct += item["severity"] == item["expected_severity"]
        cause_correct += _cause_matches(item["expected_cause"], item["likely_cause"])
    n = len(incidents)
    return {
        "severity_accuracy": severity_correct / n if n else 0.0,
        "cause_accuracy": cause_correct / n if n else 0.0,
        "n": n,
    }


if __name__ == "__main__":
    qa_set = json.loads((EVAL_DIR / "qa_set.json").read_text())
    incidents = json.loads((EVAL_DIR / "incidents.json").read_text())
    print(json.dumps({"rag": evaluate_rag(qa_set), "triage": triage_accuracy(incidents)}, indent=2))
