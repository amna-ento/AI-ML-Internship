import json
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
EVALUATION_DIR = Path(__file__).resolve().parent

sys.path.append(str(SRC_DIR))
sys.path.append(str(EVALUATION_DIR))

from metrics import calculate_metrics
from evaluation_queries import evaluation_queries

from search.keyword_search import (
    load_chunks,
    create_keyword_index,
    keyword_search
)


TOP_K = 5

VECTOR_RESULTS_FILE = Path(
    "data/vector_search_results.json"
)

HYBRID_RESULTS_FILE = Path(
    "data/hybrid_search_results.json"
)

OUTPUT_FILE = Path(
    "data/retrieval_metrics.json"
)


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_relevant_chunk_ids(chunks, expected_document):
    return [
        chunk["chunk_id"]
        for chunk in chunks
        if chunk.get("document_id") == expected_document
    ]


def evaluate_method(results_by_query, relevant_by_query):
    all_metrics = []

    for query_id in relevant_by_query:

        retrieved_ids = results_by_query.get(
            query_id,
            []
        )

        relevant_ids = relevant_by_query[query_id]

        metrics = calculate_metrics(
            retrieved_ids,
            relevant_ids,
            k=TOP_K
        )

        all_metrics.append(metrics)

    return {
        "precision": sum(
            item["precision"]
            for item in all_metrics
        ) / len(all_metrics),

        "recall": sum(
            item["recall"]
            for item in all_metrics
        ) / len(all_metrics),

        "f1": sum(
            item["f1"]
            for item in all_metrics
        ) / len(all_metrics),

        "hit_rate": sum(
            item["hit_rate"]
            for item in all_metrics
        ) / len(all_metrics),

        "mrr": sum(
            item["mrr"]
            for item in all_metrics
        ) / len(all_metrics)
    }


def main():

    print("=" * 60)
    print("RETRIEVAL METRICS EVALUATION")
    print("=" * 60)

    chunks = load_chunks()

    print(f"Chunks loaded: {len(chunks)}")
    print(f"Queries evaluated: {len(evaluation_queries)}")
    print(f"Top K: {TOP_K}")

    relevant_by_query = {}

    for item in evaluation_queries:

        relevant_by_query[item["id"]] = (
            get_relevant_chunk_ids(
                chunks,
                item["expected_document"]
            )
        )

    print("\nLoading vector results...")
    vector_results = load_json(
        VECTOR_RESULTS_FILE
    )

    print("Loading hybrid results...")
    hybrid_results = load_json(
        HYBRID_RESULTS_FILE
    )

    keyword_results = {}

    vector_results_by_query = {}

    hybrid_results_by_query = {}

    print("\nRunning keyword search...")

    vectorizer, chunk_vectors = create_keyword_index(
        chunks
    )

    for item in evaluation_queries:

        query_id = item["id"]

        results = keyword_search(
            item["query"],
            vectorizer,
            chunk_vectors,
            chunks,
            top_k=TOP_K
        )

        keyword_results[query_id] = [
            result["chunk"]["chunk_id"]
            for result in results
        ]

    for item in vector_results:

        vector_results_by_query[item["id"]] = (
            item["chunk_ids"][:TOP_K]
        )

    for item in hybrid_results:

        hybrid_results_by_query[item["id"]] = [
            result["chunk_id"]
            for result in item["results"][:TOP_K]
        ]

    keyword_metrics = evaluate_method(
        keyword_results,
        relevant_by_query
    )

    vector_metrics = evaluate_method(
        vector_results_by_query,
        relevant_by_query
    )

    hybrid_metrics = evaluate_method(
        hybrid_results_by_query,
        relevant_by_query
    )

    final_metrics = {
        "top_k": TOP_K,
        "num_queries": len(evaluation_queries),
        "metrics": {
            "keyword": keyword_metrics,
            "vector": vector_metrics,
            "hybrid": hybrid_metrics
        }
    }

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            final_metrics,
            file,
            indent=4
        )

    print("\n" + "=" * 60)
    print("OVERALL METRICS")
    print("=" * 60)

    for method, metrics in final_metrics["metrics"].items():

        print(f"\n{method.upper()} SEARCH")
        print("-" * 40)

        print(
            f"Precision@5: {metrics['precision']:.4f}"
        )

        print(
            f"Recall@5:    {metrics['recall']:.4f}"
        )

        print(
            f"F1@5:        {metrics['f1']:.4f}"
        )

        print(
            f"Hit Rate@5:  {metrics['hit_rate']:.4f}"
        )

        print(
            f"MRR@5:       {metrics['mrr']:.4f}"
        )

    print("\n" + "=" * 60)
    print("METRICS SAVED")
    print("=" * 60)

    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
    