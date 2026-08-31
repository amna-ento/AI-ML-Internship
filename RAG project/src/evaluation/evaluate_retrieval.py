from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parents[1]
EVALUATION_DIR = Path(__file__).resolve().parent

sys.path.append(str(SRC_DIR))
sys.path.append(str(EVALUATION_DIR))

from search.keyword_search import (
    load_chunks,
    create_keyword_index,
    keyword_search
)

from evaluation_queries import evaluation_queries
from metrics import calculate_metrics


def get_relevant_chunk_ids(chunks, expected_document):
    if expected_document is None:
        return []

    return [
        chunk["chunk_id"]
        for chunk in chunks
        if chunk.get("document_id") == expected_document
    ]


def get_retrieved_chunk_ids(results):
    return [
        result["chunk"]["chunk_id"]
        for result in results
    ]


def run_keyword_search(query, vectorizer, chunk_vectors, chunks):
    return keyword_search(
        query,
        vectorizer,
        chunk_vectors,
        chunks,
        top_k=5
    )


def display_results(results):
    for rank, result in enumerate(results, start=1):
        chunk = result["chunk"]

        print(
            f"{rank}. "
            f"{chunk.get('document_id')} | "
            f"{chunk.get('title')} | "
            f"Score: {result['score']:.4f}"
        )


def run_evaluation():

    print("=" * 60)
    print("RAG RETRIEVAL EVALUATION")
    print("=" * 60)

    chunks = load_chunks()

    print(f"Chunks loaded: {len(chunks)}")

    vectorizer, chunk_vectors = create_keyword_index(chunks)

    print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
    print(f"TF-IDF matrix shape: {chunk_vectors.shape}")

    print(f"Total queries: {len(evaluation_queries)}")

    all_metrics = []

    for item in evaluation_queries:

        query = item["query"]
        expected_document = item["expected_document"]

        relevant_ids = get_relevant_chunk_ids(
            chunks,
            expected_document
        )

        print("\n" + "=" * 60)
        print(f"Query {item['id']}: {query}")
        print(f"Expected document: {expected_document}")
        print(f"Relevant chunks: {len(relevant_ids)}")
        print("=" * 60)

        results = run_keyword_search(
            query,
            vectorizer,
            chunk_vectors,
            chunks
        )

        display_results(results)

        retrieved_ids = get_retrieved_chunk_ids(results)

        metrics = calculate_metrics(
            retrieved_ids,
            relevant_ids,
            k=5
        )

        all_metrics.append(metrics)

        print("\nMETRICS")
        print("-" * 40)
        print(f"Precision@5: {metrics['precision']:.2f}")
        print(f"Recall@5:    {metrics['recall']:.2f}")
        print(f"F1@5:        {metrics['f1']:.2f}")
        print(f"Hit Rate@5:  {metrics['hit_rate']:.2f}")
        print(f"MRR@5:       {metrics['mrr']:.2f}")

    average_precision = (
        sum(m["precision"] for m in all_metrics)
        / len(all_metrics)
    )

    average_recall = (
        sum(m["recall"] for m in all_metrics)
        / len(all_metrics)
    )

    average_f1 = (
        sum(m["f1"] for m in all_metrics)
        / len(all_metrics)
    )

    average_hit_rate = (
        sum(m["hit_rate"] for m in all_metrics)
        / len(all_metrics)
    )

    average_mrr = (
        sum(m["mrr"] for m in all_metrics)
        / len(all_metrics)
    )

    print("\n" + "=" * 60)
    print("KEYWORD SEARCH OVERALL METRICS")
    print("=" * 60)

    print(f"Average Precision@5: {average_precision:.2f}")
    print(f"Average Recall@5:    {average_recall:.2f}")
    print(f"Average F1@5:        {average_f1:.2f}")
    print(f"Average Hit Rate@5:  {average_hit_rate:.2f}")
    print(f"Average MRR@5:       {average_mrr:.2f}")

    print("=" * 60)


if __name__ == "__main__":
    run_evaluation()