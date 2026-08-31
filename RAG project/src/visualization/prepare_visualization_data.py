import json
import numpy as np

with open("data/processed/embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

embeddings = np.array([item["embedding"] for item in data])

metadata = [
    {
        "chunk_id": item["chunk_id"],
        "document_id": item["document_id"],
        "title": item["title"],
        "category": item["category"]
    }
    for item in data
]

np.save("data/processed/visualization_embeddings.npy", embeddings)

with open("data/processed/visualization_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("Embeddings saved:", embeddings.shape)
print("Metadata saved:", len(metadata))
print("Categories:", len(set(item["category"] for item in metadata)))