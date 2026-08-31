import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

embeddings = np.load("data/processed/visualization_embeddings.npy")

with open("data/processed/visualization_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

categories = [item["category"] for item in metadata]
unique_categories = sorted(set(categories))

pca = PCA(n_components=2)
reduced = pca.fit_transform(embeddings)

print("PCA 1 variance:", pca.explained_variance_ratio_[0])
print("PCA 2 variance:", pca.explained_variance_ratio_[1])
print("Total variance retained:", pca.explained_variance_ratio_.sum())

plt.figure(figsize=(12, 8))

for category in unique_categories:
    indices = [i for i, c in enumerate(categories) if c == category]
    plt.scatter(
        reduced[indices, 0],
        reduced[indices, 1],
        s=10,
        alpha=0.6,
        label=category
    )

plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.title("PCA Visualization by Policy Category")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()

print("Categories:", len(unique_categories))
print("Points:", len(reduced))