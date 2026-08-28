from src.embedding.embedder import generate_embeddings
from src.vectordb.vector_store import get_collection


query = "What is the probation and confirmation policy?"

collection = get_collection()

query_embedding = generate_embeddings([query])[0]

print("Query:", query)
print("Query embedding dimensions:", len(query_embedding))

results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=10,
    include=[
        "documents",
        "metadatas",
        "distances",
    ],
)

print("\n" + "=" * 60)
print("CHROMADB QUERY RESULTS")
print("=" * 60)

for rank, i in enumerate(range(len(results["ids"][0])), start=1):

    print("\nRank:", rank)
    print("ID:", results["ids"][0][i])
    print("Title:", results["metadatas"][0][i]["title"])
    print("Distance:", results["distances"][0][i])