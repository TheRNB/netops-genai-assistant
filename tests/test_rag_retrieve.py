from src.ingest import build_index
from src.rag import retrieve


def test_retrieve_returns_relevant_runbook():
    build_index()
    hits = retrieve("cell site has high latency on backhaul", k=3)
    assert len(hits) == 3
    assert any("RB001" in h["source_doc_id"] for h in hits)


def test_retrieve_hit_has_expected_fields():
    build_index()
    hits = retrieve("packet loss on access link", k=1)
    hit = hits[0]
    assert set(hit) == {"text", "source_doc_id", "chunk_id", "distance"}
