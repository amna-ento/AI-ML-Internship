from src.query.query_rewriter import rewrite_query

from src.search.hybrid_search import (
    load_chunks,
    hybrid_search
)

import chromadb

from sentence_transformers import SentenceTransformer


CHROMA_PATH = "data/chroma"


print("=" * 60)
print("QUERY REWRITING + HYBRID SEARCH")
print("=" * 60)


chunks = load_chunks()

print(f"\nChunks loaded: {len(chunks)}")


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


rewritten_query = rewrite_query(
    query
)


print("\n" + "=" * 60)
print("QUERY TRANSFORMATION")
print("=" * 60)

print("\nOriginal Query:")
print(query)

print("\nRewritten Query:")
print(rewritten_query)


original_results = hybrid_search(
    query,
    chunks,
    model,
    collection
)


rewritten_results = hybrid_search(
    rewritten_query,
    chunks,
    model,
    collection
)


print("\n" + "=" * 60)
print("ORIGINAL QUERY RESULTS")
print("=" * 60)


for index, result in enumerate(
    original_results,
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


print("\n" + "=" * 60)
print("REWRITTEN QUERY RESULTS")
print("=" * 60)


for index, result in enumerate(
    rewritten_results,
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


print("\n" + "=" * 60)
print("TOP RESULT COMPARISON")
print("=" * 60)


if original_results:
    print(
        f"\nOriginal top result:"
        f" {original_results[0]['chunk_id']}"
    )

if rewritten_results:
    print(
        f"Rewritten top result:"
        f" {rewritten_results[0]['chunk_id']}"
    )