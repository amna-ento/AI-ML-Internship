from pathlib import Path
import sys
from metrics import calculate_metrics


SEARCH_DIR = Path(__file__).resolve().parents[1] / "search"
sys.path.append(str(SEARCH_DIR))

from search.keyword_search import (
    load_chunks,
    create_keyword_index,
    keyword_search
)

from evaluation_queries import evaluation_queries


def run_keyword_search(query, vectorizer, chunk_vectors, chunks):
    return keyword_search(
        query,
        vectorizer,
        chunk_vectors,
        chunks,
        top_k=5
    )


def display_keyword_results(results):
    print("\nKEYWORD SEARCH")
    print("-" * 40)

    for rank, result in enumerate(results, start=1):
        chunk = result["chunk"]

        print(
            f"{rank}. "
            f"{chunk.get('document_id')} | "
            f"{chunk.get('title')} | "
            f"Score: {result['score']:.4f}"
        )


def get_retrieved_chunk_ids(results):
    return [
        result["chunk"]["chunk_id"]
        for result in results
    ]


def calculate_query_metrics(results, relevant_ids):
    retrieved_ids = get_retrieved_chunk_ids(results)

    return calculate_metrics(
        retrieved_ids,
        relevant_ids,
        k=5
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
        relevant_ids = item["relevant_ids"]

        print("\n" + "=" * 60)
        print(f"Query {item['id']}: {query}")
        print("=" * 60)

        results = run_keyword_search(
            query,
            vectorizer,
            chunk_vectors,
            chunks
        )

        display_keyword_results(results)

        metrics = calculate_query_metrics(
            results,
            relevant_ids
        )

        all_metrics.append(metrics)

        print("\nMETRICS")
        print("-" * 40)
        print(f"Precision@5: {metrics['precision']:.2f}")
        print(f"Recall@5:    {metrics['recall']:.2f}")
        print(f"F1@5:        {metrics['f1']:.2f}")

    average_precision = (
        sum(metric["precision"] for metric in all_metrics)
        / len(all_metrics)
    )

    average_recall = (
        sum(metric["recall"] for metric in all_metrics)
        / len(all_metrics)
    )

    average_f1 = (
        sum(metric["f1"] for metric in all_metrics)
        / len(all_metrics)
    )

    print("\n" + "=" * 60)
    print("KEYWORD SEARCH OVERALL METRICS")
    print("=" * 60)

    print(f"Average Precision@5: {average_precision:.2f}")
    print(f"Average Recall@5:    {average_recall:.2f}")
    print(f"Average F1@5:        {average_f1:.2f}")

    print("=" * 60)


if __name__ == "__main__":
    run_evaluation()