import pytest

from src.agent import triage_zero_shot
from src.rag import answer_zero_shot


@pytest.mark.llm
def test_answer_zero_shot_has_no_sources():
    result = answer_zero_shot("What should I check for high latency on a cell site?")
    assert result["answer"]
    assert result["source_doc_ids"] == []


@pytest.mark.llm
def test_triage_zero_shot_has_no_sources():
    result = triage_zero_shot("site 12 has high latency and packet loss")
    assert result.severity in {"low", "medium", "high", "critical"}
    assert result.sources == []
