import pytest

from src.evaluate import _bleu, _rouge_l, evaluate_rag, hit_rate_at_k
from src.ingest import build_index


def test_rouge_l_identical_text_scores_high():
    assert _rouge_l("check backhaul utilization for the site", "check backhaul utilization for the site") == 1.0


def test_rouge_l_unrelated_text_scores_low():
    assert _rouge_l("check backhaul utilization for the site", "bananas are yellow fruit") < 0.2


def test_bleu_identical_text_scores_high():
    assert _bleu("check backhaul utilization for the site", "check backhaul utilization for the site") == pytest.approx(1.0, abs=0.01)


def test_bleu_unrelated_text_scores_low():
    assert _bleu("check backhaul utilization for the site", "bananas are yellow fruit") < 0.05


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
    qa_set = [{
        "question": "What should I check for high latency on a cell site?",
        "gold_doc_id": "RB001_latency",
        "reference_answer": "Check backhaul link utilization for the site over the last 24 hours.",
    }]
    metrics = evaluate_rag(qa_set)
    assert metrics["hit_rate_at_k"] == 1.0
    assert 1 <= metrics["avg_faithfulness"] <= 5
    assert 1 <= metrics["avg_relevance"] <= 5
    assert 1 <= metrics["avg_correctness"] <= 5
    assert 0 <= metrics["avg_rouge_l"] <= 1
    assert 0 <= metrics["avg_bleu"] <= 1
