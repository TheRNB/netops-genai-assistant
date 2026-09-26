import pytest

from src.llm import generate


@pytest.mark.llm
def test_llm_responds():
    reply = generate("Reply with exactly one word: OK")
    assert isinstance(reply, str)
    assert len(reply.strip()) > 0
