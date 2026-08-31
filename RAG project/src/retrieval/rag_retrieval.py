import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from sentence_transformers import SentenceTransformer
import chromadb

from src.search.hybrid_search import hybrid_search


CHUNKS_FILE = "data/processed/chunks.json"
CHROMA_PATH = "data/chroma"

TOP_K = 5

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name="rag_chunks"
)


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_content(search_results):
    retrieved_chunks = []

    for result in search_results[:TOP_K]:
        retrieved_chunks.append({
            "chunk_id": result["chunk_id"],
            "document_id": result["document_id"],
            "title": result["title"],
            "section": result["section"],
            "content": result["content"],
            "hybrid_score": result["hybrid_score"]
        })

    return retrieved_chunks


def build_context(chunks):
    context_parts = []

    for chunk in chunks:
        context = (
            f"[Document ID: {chunk['document_id']}]\n"
            f"Title: {chunk['title']}\n"
            f"Section: {chunk['section']}\n\n"
            f"{chunk['content']}"
        )

        context_parts.append(context)

    return "\n\n---\n\n".join(context_parts)


def retrieve_for_api(query, top_k=TOP_K):

    chunks = load_chunks()

    search_results = hybrid_search(
        query,
        chunks,
        model,
        collection
    )

    retrieved_chunks = []

    for result in search_results[:top_k]:
        retrieved_chunks.append({
            "chunk_id": result["chunk_id"],
            "document_id": result["document_id"],
            "title": result["title"],
            "section": result["section"],
            "content": result["content"],
            "hybrid_score": result["hybrid_score"]
        })

    context = build_context(retrieved_chunks)

    return {
        "query": query,
        "results": retrieved_chunks,
        "context": context
    }