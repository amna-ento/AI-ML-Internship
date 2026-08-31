import json
import sys
import os

from sentence_transformers import SentenceTransformer
import chromadb


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from evaluation_queries import evaluation_queries
from search.hybrid_search import hybrid_search


from evaluation_queries import evaluation_queries


CHUNKS_FILE = "data/processed/chunks/chunks.json"
CHROMA_PATH = "data/vector_db"
COLLECTION_NAME = "company_knowledge_base"


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_vector_database():
    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    return collection


def main():

    print("=" * 60)
    print("HYBRID SEARCH EVALUATION")
    print("=" * 60)

    chunks = load_chunks()

    print(f"Chunks loaded: {len(chunks)}")

    print("\nLoading embedding model...")

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    print("Embedding model loaded.")

    print("\nConnecting to ChromaDB...")

    collection = load_vector_database()

    print("ChromaDB collection loaded.")

    print(f"\nTotal queries: {len(evaluation_queries)}")

    all_results = []

    for item in evaluation_queries:

        query_id = item["id"]
        query = item["query"]
        expected_document = item["expected_document"]
        query_type = item["type"]

        results = hybrid_search(
            query,
            chunks,
            model,
            collection
        )

        retrieved_document_ids = [
            result["document_id"]
            for result in results
        ]

        result_data = {
            "id": query_id,
            "query": query,
            "type": query_type,
            "expected_document": expected_document,
            "retrieved_document_ids": retrieved_document_ids,
            "results": results
        }

        all_results.append(result_data)

        print()
        print(f"Query {query_id}: {query}")
        print("-" * 60)

        print("Type:", query_type)
        print("Expected document:", expected_document)

        print("Retrieved:")

        for rank, result in enumerate(
            results,
            start=1
        ):

            print(
                f"{rank}. "
                f"{result['chunk_id']} "
                f"-> {result['document_id']} "
                f"| Keyword: {result['keyword_score']:.4f} "
                f"| Vector: {result['vector_score']:.4f} "
                f"| Hybrid: {result['hybrid_score']:.4f}"
            )

    output_file = "data/hybrid_search_results.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_results,
            file,
            indent=4
        )

    print()
    print("=" * 60)
    print("HYBRID SEARCH EVALUATION COMPLETE")
    print("=" * 60)

    print("Results saved to:")
    print(output_file)


if __name__ == "__main__":
    main()