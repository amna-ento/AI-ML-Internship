import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

embeddings = np.load("data/processed/visualization_embeddings.npy")

reduced = PCA(n_components=2).fit_transform(embeddings)

kmeans = KMeans(
    n_clusters=12,
    random_state=42,
    n_init=10
)

labels = kmeans.fit_predict(reduced)

distances = np.linalg.norm(
    reduced - kmeans.cluster_centers_[labels],
    axis=1
)

threshold = np.percentile(distances, 99)
outliers = distances >= threshold

plt.figure(figsize=(10, 7))

plt.scatter(
    reduced[~outliers, 0],
    reduced[~outliers, 1],
    s=10,
    alpha=0.4
)

plt.scatter(
    reduced[outliers, 0],
    reduced[outliers, 1],
    s=40,
    marker="x",
    label="Potential outlier"
)

plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.title("Potential Outliers in Embedding Space")
plt.legend()
plt.tight_layout()
plt.show()