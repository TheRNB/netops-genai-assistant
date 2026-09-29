"""Prints with_rag vs zero_shot raw answer text for the counterfactual set."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import EVAL_DIR
from src.ingest import build_index
from src.rag import answer, answer_zero_shot

MODEL = "llama3.1:8b"

build_index()
qa_set = json.loads((EVAL_DIR / "counterfactual_qa.json").read_text())

for item in qa_set:
    with_rag = answer(item["question"], model=MODEL)
    zero_shot = answer_zero_shot(item["question"], model=MODEL)
    print(f"\n--- {item['question']}")
    print(f"reference: {item['reference_answer']}")
    print(f"with_rag:  {with_rag['answer']}")
    print(f"zero_shot: {zero_shot['answer']}")
