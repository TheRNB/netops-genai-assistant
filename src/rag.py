from src.config import TOP_K
from src.ingest import get_collection
from src.llm import generate

NOT_COVERED = "Not covered by available runbooks."

_SYSTEM_PROMPT = (
    "You are a network-operations assistant. Answer ONLY using the provided context. "
    f'If the context does not answer the question, reply exactly: "{NOT_COVERED}" '
    "Cite nothing else beyond what's in the context."
)


def retrieve(query: str, k: int = 4) -> list[dict]:
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=k)
    hits = []
    for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        hits.append({"text": doc, "source_doc_id": meta["source_doc_id"], "chunk_id": meta["chunk_id"], "distance": dist})
    return hits


def answer(question: str, k: int = TOP_K, model: str | None = None) -> dict:
    hits = retrieve(question, k)
    context = "\n\n".join(f"[{h['source_doc_id']}] {h['text']}" for h in hits)
    prompt = f"Context:\n{context}\n\nQuestion: {question}"
    text = generate(prompt, system=_SYSTEM_PROMPT, model=model)
    source_doc_ids = sorted({h["source_doc_id"] for h in hits})
    return {"answer": text, "source_doc_ids": source_doc_ids}
