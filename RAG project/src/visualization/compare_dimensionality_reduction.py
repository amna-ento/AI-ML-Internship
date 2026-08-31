import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap

embeddings = np.load("data/processed/visualization_embeddings.npy")

with open("data/processed/visualization_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

categories = [item["category"] for item in metadata]
unique_categories = sorted(set(categories))

pca_result = PCA(n_components=2).fit_transform(embeddings)

tsne_result = TSNE(
    n_components=2,
    random_state=42,
    perplexity=30
).fit_transform(embeddings)

umap_result = umap.UMAP(
    n_components=2,
    random_state=42
).fit_transform(embeddings)

results = [
    ("PCA", pca_result),
    ("t-SNE", tsne_result),
    ("UMAP", umap_result)
]

for name, result in results:
    plt.figure(figsize=(12, 8))

    for category in unique_categories:
        indices = [i for i, c in enumerate(categories) if c == category]
        plt.scatter(
            result[indices, 0],
            result[indices, 1],
            s=12,
            alpha=0.6,
            label=category
        )

    plt.title(f"{name} - Company Policy Embeddings")
    plt.xlabel(f"{name} dimension 1")
    plt.ylabel(f"{name} dimension 2")
    plt.legend(
        bbox_to_anchor=(1.05, 1),
        loc="upper left"
    )
    plt.tight_layout()
    plt.show()