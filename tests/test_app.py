import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.ingest import build_index

client = TestClient(app)


def test_triage_missing_field_returns_422():
    response = client.post("/triage", json={})
    assert response.status_code == 422


def test_ask_missing_field_returns_422():
    response = client.post("/ask", json={})
    assert response.status_code == 422


@pytest.mark.llm
def test_triage_endpoint_returns_structured_result():
    build_index()
    response = client.post("/triage", json={"incident": "site 12 has high latency and packet loss"})
    assert response.status_code == 200
    body = response.json()
    assert body["severity"] in {"low", "medium", "high", "critical"}
    assert body["latency_ms"] > 0


@pytest.mark.llm
def test_ask_endpoint_returns_grounded_answer():
    build_index()
    response = client.post("/ask", json={"question": "What should I check for DNS resolution failures?"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"]
    assert body["latency_ms"] > 0
