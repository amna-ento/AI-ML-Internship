from src.retrieval.hybrid_search import hybrid_search


query = "What is the probation and confirmation policy?"

results = hybrid_search(query, top_k=5)

print("Query:", query)

print("\n" + "=" * 60)
print("HYBRID SEARCH")
print("=" * 60)

for rank, result in enumerate(results, start=1):

    print(f"\nRank: {rank}")
    print("ID:", result["id"])
    print("Title:", result["metadata"]["title"])
    print("Category:", result["metadata"]["category"])
    print("Vector Score:", result["vector_score"])
    print("BM25 Score:", result["bm25_score"])
    print("Hybrid Score:", result["hybrid_score"])