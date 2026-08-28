import numpy as np
from sentence_transformers import SentenceTransformer

from src.vectordb.vector_store import get_collection


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

query = "What is the probation and confirmation policy?"

collection = get_collection()
model = SentenceTransformer(MODEL_NAME)

query_embedding = model.encode(
    query,
    normalize_embeddings=True
)

# Get the known correct HR embedding
hr = collection.get(
    ids=["HR-002_chunk_001"],
    include=["embeddings", "documents", "metadatas"]
)

hr_embedding = np.array(hr["embeddings"][0])

print("Query dimensions:", len(query_embedding))
print("HR dimensions:", len(hr_embedding))

print("\nDirect cosine similarity:")
print(np.dot(query_embedding, hr_embedding))

print("\n" + "=" * 60)
print("CHROMA QUERY USING THE SAME QUERY EMBEDDING")
print("=" * 60)

results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=10,
    include=[
        "documents",
        "metadatas",
        "distances"
    ]
)

for i in range(len(results["ids"][0])):
    print("\nRank:", i + 1)
    print("ID:", results["ids"][0][i])
    print("Title:", results["metadatas"][0][i]["title"])
    print("Distance:", results["distances"][0][i])

print("\n" + "=" * 60)
print("CHROMA QUERY USING HR EMBEDDING ITSELF")
print("=" * 60)

results = collection.query(
    query_embeddings=[hr_embedding.tolist()],
    n_results=5,
    include=[
        "documents",
        "metadatas",
        "distances"
    ]
)

for i in range(len(results["ids"][0])):
    print("\nRank:", i + 1)
    print("ID:", results["ids"][0][i])
    print("Title:", results["metadatas"][0][i]["title"])
    print("Distance:", results["distances"][0][i])