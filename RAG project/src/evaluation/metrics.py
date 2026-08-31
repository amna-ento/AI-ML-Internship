def precision_at_k(retrieved_ids, relevant_ids, k):
    retrieved = retrieved_ids[:k]

    if not retrieved:
        return 0.0

    relevant_retrieved = len(set(retrieved) & set(relevant_ids))

    return relevant_retrieved / len(retrieved)


def recall_at_k(retrieved_ids, relevant_ids, k):
    retrieved = retrieved_ids[:k]

    if not relevant_ids:
        return 0.0

    relevant_retrieved = len(set(retrieved) & set(relevant_ids))

    return relevant_retrieved / len(relevant_ids)


def f1_at_k(precision, recall):
    if precision + recall == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)


def hit_rate_at_k(retrieved_ids, relevant_ids, k):
    retrieved = retrieved_ids[:k]

    return int(
        bool(set(retrieved) & set(relevant_ids))
    )


def mrr_at_k(retrieved_ids, relevant_ids, k):
    retrieved = retrieved_ids[:k]
    relevant_ids = set(relevant_ids)

    for rank, chunk_id in enumerate(retrieved, start=1):
        if chunk_id in relevant_ids:
            return 1 / rank

    return 0.0


def calculate_metrics(retrieved_ids, relevant_ids, k=5):
    precision = precision_at_k(
        retrieved_ids,
        relevant_ids,
        k
    )

    recall = recall_at_k(
        retrieved_ids,
        relevant_ids,
        k
    )

    f1 = f1_at_k(
        precision,
        recall
    )

    hit_rate = hit_rate_at_k(
        retrieved_ids,
        relevant_ids,
        k
    )

    mrr = mrr_at_k(
        retrieved_ids,
        relevant_ids,
        k
    )

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "hit_rate": hit_rate,
        "mrr": mrr
    }