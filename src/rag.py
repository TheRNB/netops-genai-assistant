from src.ingest import get_collection


def retrieve(query: str, k: int = 4) -> list[dict]:
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=k)
    hits = []
    for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        hits.append({"text": doc, "source_doc_id": meta["source_doc_id"], "chunk_id": meta["chunk_id"], "distance": dist})
    return hits
