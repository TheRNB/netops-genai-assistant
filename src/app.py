import time

from fastapi import FastAPI
from pydantic import BaseModel

from src.agent import extract_site_id
from src.agent import triage as run_triage
from src.rag import answer as run_answer

app = FastAPI(title="NetOps GenAI Assistant")


class TriageRequest(BaseModel):
    incident: str


class AskRequest(BaseModel):
    question: str


def _log(endpoint: str, latency_ms: float, **extra):
    print(f"[{endpoint}] latency_ms={latency_ms:.1f} {extra}")


@app.post("/triage")
def triage_endpoint(req: TriageRequest):
    start = time.perf_counter()
    result = run_triage(req.incident)
    latency_ms = (time.perf_counter() - start) * 1000
    _log("/triage", latency_ms, site_id=extract_site_id(req.incident), sources=result.sources)
    return {**result.model_dump(), "latency_ms": latency_ms}


@app.post("/ask")
def ask_endpoint(req: AskRequest):
    start = time.perf_counter()
    result = run_answer(req.question)
    latency_ms = (time.perf_counter() - start) * 1000
    _log("/ask", latency_ms, sources=result["source_doc_ids"])
    return {**result, "latency_ms": latency_ms}
