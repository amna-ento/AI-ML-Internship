import numpy as np

from src.vectordb.vector_store import get_collection


collection = get_collection()

ids = [
    "HR-002_chunk_001",
    "HR-002_chunk_002",
    "CB-010_chunk_002",
    "LA-021_chunk_002",
]

results = collection.get(
    ids=ids,
    include=["embeddings", "documents", "metadatas"]
)

print("Collection:", collection.name)
print("Total chunks:", collection.count())

print("\n" + "=" * 60)
print("STORED EMBEDDING CHECK")
print("=" * 60)

for i, doc_id in enumerate(results["ids"]):

    embedding = np.array(results["embeddings"][i])

    print("\nID:", doc_id)
    print("Title:", results["metadatas"][i]["title"])
    print("Dimensions:", len(embedding))
    print("First 5 values:", embedding[:5])
    print("Norm:", np.linalg.norm(embedding))