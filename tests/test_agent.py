import pytest

from src.agent import extract_site_id, kpi_lookup, triage
from src.evaluate import triage_accuracy
from src.ingest import build_index


def test_extract_site_id_variants():
    assert extract_site_id("site 12 has high latency") == "site_12"
    assert extract_site_id("site_07 packet loss") == "site_07"
    assert extract_site_id("no site mentioned here") is None


def test_kpi_lookup_known_site_returns_metrics():
    result = kpi_lookup("site_07")
    assert result["found"] is True
    assert "latest_latency_ms" in result
    assert "recent_incidents" in result


def test_kpi_lookup_unknown_site():
    result = kpi_lookup("site_99")
    assert result == {"site_id": "site_99", "found": False}


@pytest.mark.llm
def test_triage_returns_valid_structured_json():
    build_index()
    result = triage("site 12 has high latency and packet loss on its backhaul link")
    assert result.severity in {"low", "medium", "high", "critical"}
    assert result.likely_cause
    assert len(result.recommended_steps) > 0
    assert len(result.sources) > 0
    assert all(s.startswith("RB") for s in result.sources)  # sources must be real doc ids, not LLM paraphrase


@pytest.mark.llm
def test_triage_accuracy_produces_fractions():
    build_index()
    incidents = [{"incident_text": "Site 03 backhaul link shows link down.", "expected_cause": "backhaul_failure", "expected_severity": "critical"}]
    metrics = triage_accuracy(incidents)
    assert 0 <= metrics["severity_accuracy"] <= 1
    assert 0 <= metrics["cause_accuracy"] <= 1
    assert metrics["n"] == 1
