import json
import chromadb
from sentence_transformers import SentenceTransformer

from evaluation_queries import evaluation_queries


CHROMA_PATH = "data/vector_db"
COLLECTION_NAME = "company_knowledge_base"
MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 5


def load_vector_search():
    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        COLLECTION_NAME
    )

    return model, collection


def search_vector(query, model, collection):
    query_embedding = model.encode(
        query
    ).tolist()

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )


def get_document_id(chunk_id):
    return chunk_id.rsplit("-chunk-", 1)[0]


def main():

    print("=" * 60)
    print("VECTOR SEARCH EVALUATION")
    print("=" * 60)

    model, collection = load_vector_search()

    print(f"Vector database count: {collection.count()}")
    print(f"Total queries: {len(evaluation_queries)}")
    print(f"Top K: {TOP_K}")

    all_results = []

    for item in evaluation_queries:

        query_id = item["id"]
        query = item["query"]
        expected_document = item["expected_document"]
        query_type = item["type"]

        results = search_vector(
            query,
            model,
            collection
        )

        chunk_ids = results["ids"][0]
        distances = results["distances"][0]

        retrieved_document_ids = [
            get_document_id(chunk_id)
            for chunk_id in chunk_ids
        ]

        result = {
            "id": query_id,
            "query": query,
            "type": query_type,
            "expected_document": expected_document,
            "retrieved_document_ids": retrieved_document_ids,
            "chunk_ids": chunk_ids,
            "distances": distances
        }

        all_results.append(result)

        print()
        print(f"Query {query_id}: {query}")
        print("-" * 60)

        print("Type:", query_type)
        print("Expected document:", expected_document)

        print("Retrieved:")

        for rank in range(len(chunk_ids)):

            print(
                f"{rank + 1}. "
                f"{chunk_ids[rank]} "
                f"-> {retrieved_document_ids[rank]} "
                f"(distance: {distances[rank]:.4f})"
            )

    output_file = "data/vector_search_results.json"

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
    print("VECTOR SEARCH EVALUATION COMPLETE")
    print("=" * 60)

    print("Results saved to:")
    print(output_file)


if __name__ == "__main__":
    main()