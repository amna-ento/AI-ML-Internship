from rank_bm25 import BM25Okapi

from src.ingestion.loader import get_documents
from src.chunking.chunker import chunk_documents


def tokenize(text):
    """Convert text into lowercase tokens."""
    return text.lower().split()


def build_bm25_index():
    """Build a BM25 index over all document chunks."""

    documents = get_documents()
    chunks = chunk_documents(documents)

    tokenized_chunks = [
        tokenize(chunk["text"])
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_chunks)

    return bm25, chunks


def keyword_search(query, top_k=5):
    """Search chunks using BM25 keyword matching."""

    bm25, chunks = build_bm25_index()

    query_tokens = tokenize(query)

    scores = bm25.get_scores(query_tokens)

    ranked_indices = scores.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:
        results.append({
            "id": chunks[index]["chunk_id"],
            "text": chunks[index]["text"],
            "metadata": {
                "document_id": chunks[index]["document_id"],
                "title": chunks[index]["title"],
                "category": chunks[index]["category"],
                "source": chunks[index]["source"],
                "effective_date": chunks[index]["effective_date"],
                "last_updated": chunks[index]["last_updated"],
                "department": chunks[index]["department"],
            },
            "score": float(scores[index]),
        })

    return results