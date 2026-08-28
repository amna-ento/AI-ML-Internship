from src.retrieval.keyword_search import build_bm25_index, tokenize
from src.embedding.embedder import generate_embeddings
from src.vectordb.vector_store import get_collection


VECTOR_WEIGHT = 0.7
BM25_WEIGHT = 0.3


def normalize_scores(scores):
    """Normalize scores to the range 0-1."""

    minimum = min(scores)
    maximum = max(scores)

    if maximum == minimum:
        return [1.0 for _ in scores]

    return [
        (score - minimum) / (maximum - minimum)
        for score in scores
    ]


def hybrid_search(query, top_k=5):
    """Combine vector search and BM25 keyword search."""

    # --------------------------------------------------
    # 1. Vector Search
    # --------------------------------------------------

    query_embedding = generate_embeddings([query])[0]

    collection = get_collection()

    vector_results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    vector_data = {}

    for i, chunk_id in enumerate(vector_results["ids"][0]):

        vector_data[chunk_id] = {
            "id": chunk_id,
            "text": vector_results["documents"][0][i],
            "metadata": vector_results["metadatas"][0][i],
            "distance": vector_results["distances"][0][i]
        }

    # --------------------------------------------------
    # 2. BM25 Search
    # --------------------------------------------------

    bm25, chunks = build_bm25_index()

    query_tokens = tokenize(query)

    bm25_scores = bm25.get_scores(query_tokens)

    bm25_indices = bm25_scores.argsort()[::-1][:top_k]

    bm25_data = {}

    for index in bm25_indices:

        chunk = chunks[index]

        bm25_data[chunk["chunk_id"]] = {
            "id": chunk["chunk_id"],
            "text": chunk["text"],
            "metadata": {
                "document_id": chunk["document_id"],
                "title": chunk["title"],
                "category": chunk["category"],
                "source": chunk["source"],
                "effective_date": chunk["effective_date"],
                "last_updated": chunk["last_updated"],
                "department": chunk["department"],
            },
            "bm25_score": float(bm25_scores[index])
        }

    # --------------------------------------------------
    # 3. Collect all candidate IDs
    # --------------------------------------------------

    all_ids = set(vector_data) | set(bm25_data)

    # --------------------------------------------------
    # 4. Prepare scores
    # --------------------------------------------------

    vector_distances = [
        vector_data[chunk_id]["distance"]
        for chunk_id in all_ids
        if chunk_id in vector_data
    ]

    bm25_raw_scores = [
        bm25_data[chunk_id]["bm25_score"]
        for chunk_id in all_ids
        if chunk_id in bm25_data
    ]

    normalized_vector = normalize_scores(
        [-distance for distance in vector_distances]
    )

    normalized_bm25 = normalize_scores(bm25_raw_scores)

    vector_score_map = {}
    bm25_score_map = {}

    vector_index = 0

    for chunk_id in all_ids:

        if chunk_id in vector_data:
            vector_score_map[chunk_id] = normalized_vector[vector_index]
            vector_index += 1
        else:
            vector_score_map[chunk_id] = 0.0

    bm25_index = 0

    for chunk_id in all_ids:

        if chunk_id in bm25_data:
            bm25_score_map[chunk_id] = normalized_bm25[bm25_index]
            bm25_index += 1
        else:
            bm25_score_map[chunk_id] = 0.0

    # --------------------------------------------------
    # 5. Calculate Hybrid Score
    # --------------------------------------------------

    results = []

    for chunk_id in all_ids:

        hybrid_score = (
            VECTOR_WEIGHT * vector_score_map[chunk_id]
            +
            BM25_WEIGHT * bm25_score_map[chunk_id]
        )

        if chunk_id in vector_data:
            data = vector_data[chunk_id]
        else:
            data = bm25_data[chunk_id]

        results.append({
            "id": chunk_id,
            "text": data["text"],
            "metadata": data["metadata"],
            "vector_score": vector_score_map[chunk_id],
            "bm25_score": bm25_score_map[chunk_id],
            "hybrid_score": hybrid_score
        })

    # --------------------------------------------------
    # 6. Final Ranking
    # --------------------------------------------------

    results.sort(
        key=lambda x: x["hybrid_score"],
        reverse=True
    )

    return results[:top_k]