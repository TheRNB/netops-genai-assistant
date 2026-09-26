import pytest

from src.ingest import build_index
from src.rag import NOT_COVERED, answer


@pytest.mark.llm
def test_answer_grounded_question_cites_sources():
    build_index()
    result = answer("What should I check for high latency on a cell site?")
    assert result["answer"]
    assert "RB001_latency" in result["source_doc_ids"]


@pytest.mark.llm
def test_answer_unrelated_question_says_not_covered():
    build_index()
    result = answer("What is the capital of France?")
    assert NOT_COVERED.lower() in result["answer"].lower()
