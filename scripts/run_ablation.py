"""Ablation: full RAG+agent pipeline vs. the same LLM with no retrieval/tools at all."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import EVAL_DIR
from src.evaluate import evaluate_rag, evaluate_rag_zero_shot, triage_accuracy, triage_accuracy_zero_shot
from src.ingest import build_index

MODEL = "llama3.1:8b"

build_index()
qa_set = json.loads((EVAL_DIR / "qa_set.json").read_text())
incidents = json.loads((EVAL_DIR / "incidents.json").read_text())

results = {"model": MODEL}
out_path = EVAL_DIR / "rag_ablation.json"

results["with_rag"] = {"rag": evaluate_rag(qa_set, model=MODEL), "triage": triage_accuracy(incidents, model=MODEL)}
out_path.write_text(json.dumps(results, indent=2))  # checkpoint before starting the zero-shot half

results["zero_shot"] = {"rag": evaluate_rag_zero_shot(qa_set, model=MODEL), "triage": triage_accuracy_zero_shot(incidents, model=MODEL)}
out_path.write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
