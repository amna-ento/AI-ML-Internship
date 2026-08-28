
import numpy as np

from src.embedding.embedder import generate_embeddings
from src.vectordb.vector_store import get_collection


query = "What is the probation and confirmation policy?"

query_embedding = generate_embeddings([query])[0]

collection = get_collection()

results = collection.get(
    ids=[
        "HR-002_chunk_001",
        "CB-010_chunk_002"
    ],
    include=[
        "documents",
        "embeddings",
        "metadatas"
    ]
)

print("Query:", query)

print("\nQuery embedding dimensions:")
print(len(query_embedding))

for i in range(len(results["ids"])):

    stored_embedding = np.array(results["embeddings"][i])

    cosine_similarity = np.dot(
        query_embedding,
        stored_embedding
    ) / (
        np.linalg.norm(query_embedding)
        * np.linalg.norm(stored_embedding)
    )

    cosine_distance = 1 - cosine_similarity

    print("\n" + "=" * 60)
    print("ID:", results["ids"][i])
    print("Title:", results["metadatas"][i]["title"])

    print("\nText:")
    print(results["documents"][i])

    print("\nCosine similarity:")
    print(cosine_similarity)

    print("\nCosine distance:")
    print(cosine_distance)
