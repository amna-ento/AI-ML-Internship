import json
import numpy as np

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parents[2]

CHUNKS_FILE = BASE_DIR / "data" / "processed" / "chunks.json"


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    return chunks


def create_keyword_index(chunks):
    texts = [chunk["content"] for chunk in chunks]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )

    chunk_vectors = vectorizer.fit_transform(texts)

    return vectorizer, chunk_vectors


def keyword_search(query, vectorizer, chunk_vectors, chunks, top_k=5):
    query_vector = vectorizer.transform([query])

    scores = cosine_similarity(
        query_vector,
        chunk_vectors
    )[0]

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append({
            "chunk": chunks[index],
            "score": float(scores[index])
        })

    return results


def display_results(query, results):
    print("\n" + "=" * 60)
    print("KEYWORD SEARCH")
    print("=" * 60)

    print(f"\nQuery: {query}")
    print(f"Results returned: {len(results)}")

    for i, result in enumerate(results, start=1):
        chunk = result["chunk"]

        print(f"\n--- Result {i} ---")
        print(f"Score: {result['score']:.4f}")
        print(f"Chunk ID: {chunk.get('chunk_id')}")
        print(f"Document ID: {chunk.get('document_id')}")
        print(f"Title: {chunk.get('title')}")
        print(f"Category: {chunk.get('category')}")
        print(f"Department: {chunk.get('department')}")

        content = chunk.get("content", "")
        print(f"Content: {content[:300]}...")


def main():
    print("=" * 60)
    print("KEYWORD SEARCH SETUP")
    print("=" * 60)

    chunks = load_chunks()

    print(f"\nChunks loaded: {len(chunks)}")

    vectorizer, chunk_vectors = create_keyword_index(chunks)

    print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
    print(f"TF-IDF matrix shape: {chunk_vectors.shape}")

    query = "How do I update my emergency contact?"

    results = keyword_search(
        query,
        vectorizer,
        chunk_vectors,
        chunks,
        top_k=5
    )

    display_results(query, results)


if __name__ == "__main__":
    main()