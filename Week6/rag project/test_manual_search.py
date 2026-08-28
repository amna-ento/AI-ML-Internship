import numpy as np

from src.embedding.embedder import generate_embeddings
from src.vectordb.vector_store import get_collection


query = "What is the probation and confirmation policy?"

collection = get_collection()

query_embedding = generate_embeddings([query])[0]

results = collection.get(
    include=["embeddings", "documents", "metadatas"]
)

embeddings = np.array(results["embeddings"])

similarities = embeddings @ query_embedding

top_indices = np.argsort(similarities)[::-1][:10]

print("=" * 60)
print("MANUAL COSINE SEARCH")
print("=" * 60)

for rank, index in enumerate(top_indices, start=1):

    print(f"\nRank: {rank}")
    print("ID:", results["ids"][index])
    print("Title:", results["metadatas"][index]["title"])
    print("Similarity:", similarities[index])
    print("Distance:", 1 - similarities[index])