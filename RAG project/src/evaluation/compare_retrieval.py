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

METRICS_FILE = Path(
    "data/retrieval_metrics.json"
)

OUTPUT_FILE = Path(
    "data/retrieval_comparison.json"
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


def calculate_method_metrics(
    retrieved_ids,
    relevant_ids
):
    return calculate_metrics(
        retrieved_ids,
        relevant_ids,
        k=TOP_K
    )


def main():

    print("=" * 70)
    print("RETRIEVAL METHOD COMPARISON")
    print("=" * 70)

    chunks = load_chunks()

    vector_results = load_json(
        VECTOR_RESULTS_FILE
    )

    hybrid_results = load_json(
        HYBRID_RESULTS_FILE
    )

    metrics_summary = load_json(
        METRICS_FILE
    )

    vector_by_query = {
        item["id"]: item["chunk_ids"][:TOP_K]
        for item in vector_results
    }

    hybrid_by_query = {
        item["id"]: [
            result["chunk_id"]
            for result in item["results"][:TOP_K]
        ]
        for item in hybrid_results
    }

    print("\nBuilding keyword index...")

    vectorizer, chunk_vectors = create_keyword_index(
        chunks
    )

    keyword_by_query = {}

    for item in evaluation_queries:

        results = keyword_search(
            item["query"],
            vectorizer,
            chunk_vectors,
            chunks,
            top_k=TOP_K
        )

        keyword_by_query[item["id"]] = [
            result["chunk"]["chunk_id"]
            for result in results
        ]

    comparison = []

    for item in evaluation_queries:

        query_id = item["id"]
        query = item["query"]
        query_type = item["type"]
        expected_document = item["expected_document"]

        relevant_ids = get_relevant_chunk_ids(
            chunks,
            expected_document
        )

        keyword_metrics = calculate_method_metrics(
            keyword_by_query.get(query_id, []),
            relevant_ids
        )

        vector_metrics = calculate_method_metrics(
            vector_by_query.get(query_id, []),
            relevant_ids
        )

        hybrid_metrics = calculate_method_metrics(
            hybrid_by_query.get(query_id, []),
            relevant_ids
        )

        methods = {
            "keyword": keyword_metrics,
            "vector": vector_metrics,
            "hybrid": hybrid_metrics
        }

        best_method = max(
            methods,
            key=lambda method: methods[method]["f1"]
        )

        comparison.append({
            "id": query_id,
            "query": query,
            "type": query_type,
            "expected_document": expected_document,
            "keyword": keyword_metrics,
            "vector": vector_metrics,
            "hybrid": hybrid_metrics,
            "best_method": best_method
        })

    print("\n" + "=" * 70)
    print("QUERY-BY-QUERY COMPARISON")
    print("=" * 70)

    for item in comparison:

        print()
        print(
            f"{item['id']} | "
            f"{item['type']}"
        )

        print(
            f"Query: {item['query']}"
        )

        print(
            f"Keyword F1: {item['keyword']['f1']:.2f} | "
            f"Vector F1: {item['vector']['f1']:.2f} | "
            f"Hybrid F1: {item['hybrid']['f1']:.2f}"
        )

        print(
            f"Best: {item['best_method'].upper()}"
        )

    method_wins = {
        "keyword": 0,
        "vector": 0,
        "hybrid": 0
    }

    for item in comparison:
        method_wins[item["best_method"]] += 1

    print("\n" + "=" * 70)
    print("WIN COUNT")
    print("=" * 70)

    for method, count in method_wins.items():

        print(
            f"{method.capitalize():<10}: "
            f"{count}/{len(comparison)} queries"
        )

    type_summary = {}

    for item in comparison:

        query_type = item["type"]

        if query_type not in type_summary:
            type_summary[query_type] = {
                "keyword": [],
                "vector": [],
                "hybrid": []
            }

        type_summary[query_type]["keyword"].append(
            item["keyword"]["f1"]
        )

        type_summary[query_type]["vector"].append(
            item["vector"]["f1"]
        )

        type_summary[query_type]["hybrid"].append(
            item["hybrid"]["f1"]
        )

    print("\n" + "=" * 70)
    print("PER-QUERY-TYPE F1 COMPARISON")
    print("=" * 70)

    for query_type, methods in type_summary.items():

        print(f"\n{query_type}")

        for method, scores in methods.items():

            average = sum(scores) / len(scores)

            print(
                f"{method.capitalize():<10}: "
                f"{average:.4f}"
            )

    output = {
        "top_k": TOP_K,
        "num_queries": len(comparison),
        "overall_metrics": metrics_summary["metrics"],
        "query_comparison": comparison,
        "method_wins": method_wins,
        "query_type_summary": type_summary
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4
        )

    print("\n" + "=" * 70)
    print("COMPARISON SAVED")
    print("=" * 70)

    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()