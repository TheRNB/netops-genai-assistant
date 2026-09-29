"""Prints per-incident with_rag vs zero_shot triage output side by side, to find the disagreements."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent import triage, triage_zero_shot
from src.config import EVAL_DIR
from src.evaluate import _cause_matches
from src.ingest import build_index

MODEL = "llama3.1:8b"

build_index()
incidents = json.loads((EVAL_DIR / "incidents.json").read_text())

for item in incidents:
    with_rag = triage(item["incident_text"], model=MODEL)
    zero_shot = triage_zero_shot(item["incident_text"], model=MODEL)
    rag_cause_ok = _cause_matches(item["expected_cause"], with_rag.likely_cause)
    zs_cause_ok = _cause_matches(item["expected_cause"], zero_shot.likely_cause)
    print(f"\n--- {item['incident_text']}")
    print(f"expected: severity={item['expected_severity']} cause={item['expected_cause']}")
    print(f"with_rag:  severity={with_rag.severity} ({'OK' if with_rag.severity==item['expected_severity'] else 'X'})  cause={with_rag.likely_cause[:90]!r} ({'OK' if rag_cause_ok else 'X'})  sources={with_rag.sources}")
    print(f"zero_shot: severity={zero_shot.severity} ({'OK' if zero_shot.severity==item['expected_severity'] else 'X'})  cause={zero_shot.likely_cause[:90]!r} ({'OK' if zs_cause_ok else 'X'})")
