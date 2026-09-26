import json

from src.config import EVAL_DIR, RUNBOOKS_DIR

VALID_SEVERITIES = {"low", "medium", "high", "critical"}


def _runbook_ids():
    return {p.stem for p in RUNBOOKS_DIR.glob("*.md")}


def test_qa_set_well_formed_and_grounded():
    qa_set = json.loads((EVAL_DIR / "qa_set.json").read_text())
    assert len(qa_set) >= 30
    runbook_ids = _runbook_ids()
    for item in qa_set:
        assert {"question", "reference_answer", "gold_doc_id"} <= item.keys()
        assert item["gold_doc_id"] in runbook_ids


def test_incidents_well_formed():
    incidents = json.loads((EVAL_DIR / "incidents.json").read_text())
    assert len(incidents) >= 15
    for item in incidents:
        assert {"incident_text", "expected_cause", "expected_severity"} <= item.keys()
        assert item["expected_severity"] in VALID_SEVERITIES
