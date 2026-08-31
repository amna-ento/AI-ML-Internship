import json
import re

import chromadb
from sentence_transformers import SentenceTransformer


CHUNKS_FILE = "data/processed/chunks.json"
CHROMA_PATH = "data/chroma"

KEYWORD_WEIGHT = 0.5
VECTOR_WEIGHT = 0.5

KEYWORD_TOP_K = 10
VECTOR_TOP_K = 10
FINAL_TOP_K = 5


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def tokenize(text):
    return set(re.findall(r"\b\w+\b", text.lower()))


def keyword_score(query, content):
    query_words = tokenize(query)
    content_words = tokenize(content)

    if not query_words:
        return 0.0

    matched_words = query_words.intersection(content_words)

    return len(matched_words) / len(query_words)


def normalize_scores(scores):
    if not scores:
        return []

    minimum = min(scores)
    maximum = max(scores)

    if maximum == minimum:
        return [1.0] * len(scores)

    return [
        (score - minimum) / (maximum - minimum)
        for score in scores
    ]


def perform_keyword_search(query, chunks):
    results = []

    for chunk in chunks:
        score = keyword_score(
            query,
            chunk["content"]
        )

        if score > 0:
            results.append({
                "chunk_id": chunk["chunk_id"],
                "keyword_score": score
            })

    results.sort(
        key=lambda result: result["keyword_score"],
        reverse=True
    )

    return results[:KEYWORD_TOP_K]


def perform_vector_search(query, model, collection):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=VECTOR_TOP_K,
        include=["documents", "distances"]
    )

    ids = results["ids"][0]

    distances = results.get("distances")

    if distances is not None:
        distances = distances[0]

        similarities = [
            1 / (1 + distance)
            for distance in distances
        ]

        similarities = normalize_scores(similarities)

    else:
        similarities = [
            1.0 for _ in ids
        ]

    vector_results = []

    for i, chunk_id in enumerate(ids):
        vector_results.append({
            "chunk_id": chunk_id,
            "vector_score": similarities[i]
        })

    return vector_results


def hybrid_search(query, chunks, model, collection):
    keyword_results = perform_keyword_search(
        query,
        chunks
    )

    vector_results = perform_vector_search(
        query,
        model,
        collection
    )

    candidates = {}

    for result in keyword_results:
        chunk_id = result["chunk_id"]

        candidates[chunk_id] = {
            "chunk_id": chunk_id,
            "keyword_score": result["keyword_score"],
            "vector_score": 0.0
        }

    for result in vector_results:
        chunk_id = result["chunk_id"]

        if chunk_id not in candidates:
            candidates[chunk_id] = {
                "chunk_id": chunk_id,
                "keyword_score": 0.0,
                "vector_score": result["vector_score"]
            }

        else:
            candidates[chunk_id]["vector_score"] = (
                result["vector_score"]
            )

    chunk_map = {
        chunk["chunk_id"]: chunk
        for chunk in chunks
    }

    final_results = []

    for chunk_id, candidate in candidates.items():

        chunk = chunk_map.get(chunk_id)

        if not chunk:
            continue

        keyword = candidate["keyword_score"]
        vector = candidate["vector_score"]

        hybrid = (
            KEYWORD_WEIGHT * keyword
            +
            VECTOR_WEIGHT * vector
        )

        final_results.append({
            "chunk_id": chunk_id,
            "document_id": chunk["document_id"],
            "title": chunk["title"],
            "section": chunk["section"],
            "keyword_score": keyword,
            "vector_score": vector,
            "hybrid_score": hybrid,
            "content": chunk["content"]
        })

    final_results.sort(
        key=lambda result: result["hybrid_score"],
        reverse=True
    )

    return final_results[:FINAL_TOP_K]


def main():
    print("=" * 60)
    print("HYBRID SEARCH")
    print("=" * 60)

    chunks = load_chunks()

    print(f"Chunks loaded: {len(chunks)}")

    print("\nLoading embedding model...")

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    print("Embedding model loaded.")

    print("\nConnecting to ChromaDB...")

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name="rag_chunks"
    )

    print("ChromaDB collection loaded.")

    query = input(
        "\nEnter your search query: "
    )

    results = hybrid_search(
        query,
        chunks,
        model,
        collection
    )

    print("\n" + "=" * 60)
    print("HYBRID SEARCH RESULTS")
    print("=" * 60)

    print(f"\nQuery: {query}")

    for index, result in enumerate(
        results,
        start=1
    ):

        print("\n" + "-" * 60)
        print(f"Result {index}")
        print("-" * 60)

        print(
            f"Chunk ID:      {result['chunk_id']}"
        )

        print(
            f"Document ID:   {result['document_id']}"
        )

        print(
            f"Title:         {result['title']}"
        )

        print(
            f"Section:       {result['section']}"
        )

        print(
            f"Keyword Score: {result['keyword_score']:.4f}"
        )

        print(
            f"Vector Score:  {result['vector_score']:.4f}"
        )

        print(
            f"Hybrid Score:  {result['hybrid_score']:.4f}"
        )

        print("\nContent:")

        print(
            result["content"][:500]
        )


if __name__ == "__main__":
    main()