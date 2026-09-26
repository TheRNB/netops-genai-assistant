import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from src.config import CHROMA_DIR, CHUNK_OVERLAP, CHUNK_SIZE, EMBED_MODEL, RUNBOOKS_DIR

COLLECTION_NAME = "runbooks"


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c for c in chunks if c.strip()]


def get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
    return client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embed_fn)


def build_index() -> int:
    collection = get_collection()
    ids, docs, metadatas = [], [], []
    for path in sorted(RUNBOOKS_DIR.glob("*.md")):
        source_doc_id = path.stem
        text = path.read_text()
        for i, chunk in enumerate(chunk_text(text)):
            ids.append(f"{source_doc_id}_{i}")
            docs.append(chunk)
            metadatas.append({"source_doc_id": source_doc_id, "chunk_id": i})

    if ids:
        collection.upsert(ids=ids, documents=docs, metadatas=metadatas)
    return len(ids)


if __name__ == "__main__":
    n = build_index()
    print(f"Indexed {n} chunks")
