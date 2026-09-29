"""Knowledge-conflict ablation: correct answer deliberately contradicts generic advice."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import EVAL_DIR
from src.evaluate import evaluate_rag, evaluate_rag_zero_shot
from src.ingest import build_index

MODEL = "llama3.1:8b"

build_index()
qa_set = json.loads((EVAL_DIR / "counterfactual_qa.json").read_text())

results = {"model": MODEL}
out_path = EVAL_DIR / "counterfactual_ablation.json"

results["with_rag"] = evaluate_rag(qa_set, model=MODEL)
out_path.write_text(json.dumps(results, indent=2))  # checkpoint before starting the zero-shot half

results["zero_shot"] = evaluate_rag_zero_shot(qa_set, model=MODEL)
out_path.write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
