import json
import numpy as np

with open("data/processed/embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

embeddings = np.array([item["embedding"] for item in data])

print("Embedding shape:", embeddings.shape)
print("Number of embeddings:", len(embeddings))
print("Embedding dimensions:", embeddings.shape[1])
print("Number of chunks:", len(data))

print("\nAlignment check:")
print("PASS" if len(data) == embeddings.shape[0] else "FAIL")