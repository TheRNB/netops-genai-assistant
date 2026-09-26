import json

import pytest

from src.config import EVAL_DIR
from src.llm import generate

REQUIRED_MODELS = {"llama3.1:8b", "deepseek-r1:8b", "qwen2.5:14b", "deepseek-r1:14b", "mistral-nemo:12b", "gemma2:9b"}


def test_model_comparison_file_well_formed():
    data = json.loads((EVAL_DIR / "model_comparison.json").read_text())
    assert REQUIRED_MODELS <= data.keys()
    for model, result in data.items():
        assert 0 <= result["rag"]["hit_rate_at_k"] <= 1
        assert 1 <= result["rag"]["avg_faithfulness"] <= 5
        assert 0 <= result["triage"]["severity_accuracy"] <= 1
        assert 0 <= result["triage"]["cause_accuracy"] <= 1
        assert result["elapsed_sec"] > 0


@pytest.mark.llm
def test_generate_respects_model_override():
    reply = generate("Reply with exactly one word: OK", model="gemma2:9b")
    assert isinstance(reply, str) and reply.strip()
