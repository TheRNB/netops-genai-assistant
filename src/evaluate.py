import json
import re

from src.config import EVAL_DIR
from src.llm import generate
from src.rag import answer, retrieve

# ragas 0.2.10 fails to import against the installed langchain-community version
# (missing ChatVertexAI), so we score faithfulness/relevance with a direct LLM-judge prompt instead.
_JUDGE_PROMPT = (
    "Rate the ANSWER on a 1-5 scale for {aspect} given the QUESTION and CONTEXT. "
    "Reply with ONLY the integer.\n\nQUESTION: {question}\nCONTEXT: {context}\nANSWER: {answer}"
)


def _judge_score(question: str, context: str, answer_text: str, aspect: str) -> int:
    prompt = _JUDGE_PROMPT.format(aspect=aspect, question=question, context=context, answer=answer_text)
    reply = generate(prompt)
    match = re.search(r"[1-5]", reply)
    return int(match.group()) if match else 1


def hit_rate_at_k(qa_set: list[dict], k: int = 4) -> float:
    hits = 0
    for item in qa_set:
        retrieved_ids = {h["source_doc_id"] for h in retrieve(item["question"], k=k)}
        if item["gold_doc_id"] in retrieved_ids:
            hits += 1
    return hits / len(qa_set) if qa_set else 0.0


def evaluate_rag(qa_set: list[dict]) -> dict:
    faithfulness_scores, relevance_scores = [], []
    for item in qa_set:
        result = answer(item["question"])
        context = "\n".join(h["text"] for h in retrieve(item["question"]))
        faithfulness_scores.append(_judge_score(item["question"], context, result["answer"], "faithfulness to the context"))
        relevance_scores.append(_judge_score(item["question"], context, result["answer"], "relevance to the question"))

    return {
        "hit_rate_at_k": hit_rate_at_k(qa_set),
        "avg_faithfulness": sum(faithfulness_scores) / len(faithfulness_scores),
        "avg_relevance": sum(relevance_scores) / len(relevance_scores),
        "n": len(qa_set),
    }


if __name__ == "__main__":
    qa_set = json.loads((EVAL_DIR / "qa_set.json").read_text())
    metrics = evaluate_rag(qa_set)
    print(json.dumps(metrics, indent=2))
