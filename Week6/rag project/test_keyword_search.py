from src.retrieval.keyword_search import keyword_search


query = "What is the probation and confirmation policy?"

results = keyword_search(query, top_k=5)

print("Query:", query)

print("\n" + "=" * 60)
print("BM25 KEYWORD SEARCH")
print("=" * 60)

for rank, result in enumerate(results, start=1):

    print(f"\nRank: {rank}")
    print("ID:", result["id"])
    print("Title:", result["metadata"]["title"])
    print("Category:", result["metadata"]["category"])
    print("BM25 Score:", result["score"])