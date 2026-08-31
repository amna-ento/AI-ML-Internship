import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

embeddings = np.load("data/processed/visualization_embeddings.npy")

with open("data/processed/visualization_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

categories = [item["category"] for item in metadata]
unique_categories = sorted(set(categories))

tsne = TSNE(
    n_components=2,
    random_state=42,
    perplexity=30
)

reduced = tsne.fit_transform(embeddings)

plt.figure(figsize=(12, 8))

for category in unique_categories:
    indices = [i for i, c in enumerate(categories) if c == category]

    plt.scatter(
        reduced[indices, 0],
        reduced[indices, 1],
        s=12,
        alpha=0.65,
        label=category
    )

plt.xlabel("t-SNE dimension 1")
plt.ylabel("t-SNE dimension 2")
plt.title("t-SNE Map of Company Policy Embeddings")
plt.legend(
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
    title="Policy Category"
)

plt.tight_layout()
plt.show()

print("Number of categories:", len(unique_categories))
print("Number of chunks:", len(reduced))