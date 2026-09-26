import pytest

from src.evaluate import evaluate_rag, hit_rate_at_k
from src.ingest import build_index


def test_hit_rate_at_k_all_correct():
    build_index()
    qa_set = [{"question": "high latency on a cell site backhaul", "gold_doc_id": "RB001_latency"}]
    assert hit_rate_at_k(qa_set, k=4) == 1.0


def test_hit_rate_at_k_impossible_gold_doc():
    build_index()
    qa_set = [{"question": "high latency on a cell site backhaul", "gold_doc_id": "NOT_A_REAL_DOC"}]
    assert hit_rate_at_k(qa_set, k=4) == 0.0


def test_hit_rate_at_k_empty_set():
    assert hit_rate_at_k([], k=4) == 0.0


@pytest.mark.llm
def test_evaluate_rag_produces_numeric_metrics():
    build_index()
    qa_set = [{"question": "What should I check for high latency on a cell site?", "gold_doc_id": "RB001_latency"}]
    metrics = evaluate_rag(qa_set)
    assert metrics["hit_rate_at_k"] == 1.0
    assert 1 <= metrics["avg_faithfulness"] <= 5
    assert 1 <= metrics["avg_relevance"] <= 5
