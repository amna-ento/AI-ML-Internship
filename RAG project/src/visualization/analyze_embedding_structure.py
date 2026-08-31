import json
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

embeddings = np.load("data/processed/visualization_embeddings.npy")

with open("data/processed/visualization_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

categories = [item["category"] for item in metadata]

pca = PCA(n_components=2)
reduced = pca.fit_transform(embeddings)

kmeans = KMeans(n_clusters=12, random_state=42, n_init=10)
labels = kmeans.fit_predict(reduced)

score = silhouette_score(reduced, labels)

distances = np.linalg.norm(
    reduced - kmeans.cluster_centers_[labels],
    axis=1
)

outlier_indices = np.argsort(distances)[-10:]

print("=" * 60)
print("EMBEDDING STRUCTURE ANALYSIS")
print("=" * 60)

print(f"Clusters: 12")
print(f"Silhouette score: {score:.4f}")

print("\nTop 10 potential outliers:")

for index in outlier_indices[::-1]:
    print(
        f"- {metadata[index]['chunk_id']} | "
        f"{metadata[index]['category']} | "
        f"{metadata[index]['title']}"
    )

print("\nCluster distribution:")

for cluster in range(12):
    count = np.sum(labels == cluster)
    print(f"Cluster {cluster}: {count} chunks")