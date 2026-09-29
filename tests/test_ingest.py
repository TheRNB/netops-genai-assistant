from src.ingest import build_index, chunk_text


def test_chunk_text_respects_size_and_overlap():
    text = "x" * 1200
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) >= 2
    assert all(len(c) <= 500 for c in chunks)


def test_chunk_text_empty_string():
    assert chunk_text("") == []


def test_chunk_text_no_redundant_trailing_chunk_when_text_fits():
    text = "x" * 900
    chunks = chunk_text(text, chunk_size=1000, overlap=100)
    assert len(chunks) == 1


def test_build_index_returns_positive_chunk_count():
    n = build_index()
    assert n > 0
