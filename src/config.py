import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
RUNBOOKS_DIR = DATA_DIR / "runbooks"
OPS_KPI_CSV = DATA_DIR / "ops_kpis.csv"
CHROMA_DIR = ROOT_DIR / "chroma_db"
EVAL_DIR = ROOT_DIR / "eval"
REPORTS_DIR = ROOT_DIR / "reports"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 4

EMBED_MODEL = "all-MiniLM-L6-v2"

LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1:8b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
