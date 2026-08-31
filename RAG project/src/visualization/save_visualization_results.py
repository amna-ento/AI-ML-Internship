import json
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap

embeddings = np.load("data/processed/visualization_embeddings.npy")

with open("data/processed/visualization_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

pca = PCA(n_components=2)
pca_result = pca.fit_transform(embeddings)

tsne = TSNE(n_components=2, random_state=42, perplexity=30)
tsne_result = tsne.fit_transform(embeddings)

umap_result = umap.UMAP(n_components=2, random_state=42).fit_transform(embeddings)

results = []

for i, item in enumerate(metadata):
    results.append({
        "chunk_id": item["chunk_id"],
        "document_id": item["document_id"],
        "title": item["title"],
        "category": item["category"],
        "pca_x": float(pca_result[i, 0]),
        "pca_y": float(pca_result[i, 1]),
        "tsne_x": float(tsne_result[i, 0]),
        "tsne_y": float(tsne_result[i, 1]),
        "umap_x": float(umap_result[i, 0]),
        "umap_y": float(umap_result[i, 1])
    })

with open("data/processed/visualization_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f)

print("Saved:", len(results), "embedding points")
print("Output: data/processed/visualization_results.json")