import json
import re
from typing import Literal

import pandas as pd
from pydantic import BaseModel

from src.config import OPS_KPI_CSV
from src.llm import generate
from src.rag import retrieve

SITE_ID_PATTERN = re.compile(r"site[_\s]?(\d+)", re.IGNORECASE)


class Triage(BaseModel):
    severity: Literal["low", "medium", "high", "critical"]
    likely_cause: str
    recommended_steps: list[str]
    sources: list[str]


def extract_site_id(text: str) -> str | None:
    match = SITE_ID_PATTERN.search(text)
    return f"site_{int(match.group(1)):02d}" if match else None


def doc_retrieval(query: str, k: int = 4) -> list[dict]:
    return retrieve(query, k=k)


def kpi_lookup(site_id: str, recent_n: int = 24) -> dict:
    df = pd.read_csv(OPS_KPI_CSV)
    site_df = df[df["site_id"] == site_id].tail(recent_n)
    if site_df.empty:
        return {"site_id": site_id, "found": False}
    latest = site_df.iloc[-1]
    recent_incidents = sorted(set(site_df["incident_label"]) - {"none"})
    return {
        "site_id": site_id,
        "found": True,
        "latest_latency_ms": float(latest["latency_ms"]),
        "latest_throughput_mbps": float(latest["throughput_mbps"]),
        "latest_packet_loss_pct": float(latest["packet_loss_pct"]),
        "recent_incidents": recent_incidents,
    }


_TRIAGE_SYSTEM_PROMPT = (
    "You are a network-operations triage assistant. Using the runbook context and KPI context "
    "given, respond with ONLY a JSON object matching this schema: "
    '{"severity": "low|medium|high|critical", "likely_cause": str, '
    '"recommended_steps": [str, ...], "sources": [str, ...]}. No prose outside the JSON.'
)


def triage(incident_text: str, model: str | None = None) -> Triage:
    hits = doc_retrieval(incident_text)
    runbook_context = "\n\n".join(f"[{h['source_doc_id']}] {h['text']}" for h in hits)
    source_ids = sorted({h["source_doc_id"] for h in hits})

    site_id = extract_site_id(incident_text)
    kpi_context = json.dumps(kpi_lookup(site_id)) if site_id else "No site_id mentioned in the incident."

    prompt = (
        f"Incident: {incident_text}\n\nRunbook context:\n{runbook_context}\n\nKPI context:\n{kpi_context}"
    )
    reply = generate(prompt, system=_TRIAGE_SYSTEM_PROMPT, model=model)
    match = re.search(r"\{.*\}", reply, re.DOTALL)
    data = json.loads(match.group()) if match else json.loads(reply)
    data["sources"] = source_ids  # always cite the actually-retrieved docs, not the LLM's own claim
    return Triage(**data)


if __name__ == "__main__":
    import sys

    result = triage(" ".join(sys.argv[1:]))
    print(result.model_dump_json(indent=2))
