"""Runs the eval suite once per candidate model and writes eval/model_comparison.json."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import EVAL_DIR
from src.evaluate import evaluate_rag, triage_accuracy
from src.ingest import build_index

MODELS = [
    "llama3.1:8b",
    "deepseek-r1:8b",
    "qwen2.5:14b",
    "deepseek-r1:14b",
    "mistral-nemo:12b",
    "gemma2:9b",
]

build_index()
qa_set = json.loads((EVAL_DIR / "qa_set.json").read_text())
incidents = json.loads((EVAL_DIR / "incidents.json").read_text())

results = {}
for model in MODELS:
    print(f"=== {model} ===")
    start = time.perf_counter()
    rag_metrics = evaluate_rag(qa_set, model=model)
    triage_metrics = triage_accuracy(incidents, model=model)
    elapsed = time.perf_counter() - start
    results[model] = {"rag": rag_metrics, "triage": triage_metrics, "elapsed_sec": round(elapsed, 1)}
    print(json.dumps(results[model], indent=2))

(EVAL_DIR / "model_comparison.json").write_text(json.dumps(results, indent=2))
print(f"\nWrote {EVAL_DIR / 'model_comparison.json'}")
