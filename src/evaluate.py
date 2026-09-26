import json
import re

from src.agent import triage
from src.config import EVAL_DIR
from src.llm import generate
from src.rag import answer, retrieve

# ragas 0.2.10 won't import here (missing ChatVertexAI), so we just prompt the LLM to judge directly.
_JUDGE_PROMPT = (
    "Rate the ANSWER on a 1-5 scale for {aspect} given the QUESTION and CONTEXT. "
    "Reply with ONLY the integer.\n\nQUESTION: {question}\nCONTEXT: {context}\nANSWER: {answer}"
)

# Fixed so every model is graded by the same judge.
JUDGE_MODEL = "llama3.1:8b"


def _judge_score(question: str, context: str, answer_text: str, aspect: str) -> int:
    prompt = _JUDGE_PROMPT.format(aspect=aspect, question=question, context=context, answer=answer_text)
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
    faithfulness_scores, relevance_scores = [], []
    for item in qa_set:
        result = answer(item["question"], model=model)
        context = "\n".join(h["text"] for h in retrieve(item["question"]))
        faithfulness_scores.append(_judge_score(item["question"], context, result["answer"], "faithfulness to the context"))
        relevance_scores.append(_judge_score(item["question"], context, result["answer"], "relevance to the question"))

    return {
        "hit_rate_at_k": hit_rate_at_k(qa_set),
        "avg_faithfulness": sum(faithfulness_scores) / len(faithfulness_scores),
        "avg_relevance": sum(relevance_scores) / len(relevance_scores),
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
    severity_correct, cause_correct = 0, 0
    for item in incidents:
        result = triage(item["incident_text"], model=model)
        severity_correct += result.severity == item["expected_severity"]
        cause_correct += _cause_matches(item["expected_cause"], result.likely_cause)
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
