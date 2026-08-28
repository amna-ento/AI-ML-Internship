from src.embedding.embedder import generate_embeddings
from src.vectordb.vector_store import get_collection


def vector_search(query, top_k=5):
    query_embedding = generate_embeddings([query])[0]

    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    retrieved_results = []

    for i in range(len(results["ids"][0])):
        retrieved_results.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return retrieved_results