import json
import re
from pathlib import Path

from evaluation_queries import evaluation_queries


DATASET_PATH = Path(
    "data/raw/company_policies_rag_10_10_FINAL(1).json"
)


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def tokenize(text):
    return set(re.findall(r"\b[a-zA-Z]{3,}\b", text.lower()))


def document_text(document):
    fields = [
        document.get("title", ""),
        document.get("category", ""),
        document.get("subcategory", ""),
        " ".join(document.get("keywords", [])),
        " ".join(document.get("aliases", [])),
        " ".join(document.get("topics", [])),
        " ".join(document.get("entities", [])),
        " ".join(document.get("common_questions", [])),
        document.get("content", "")
    ]

    return " ".join(fields)


def calculate_overlap(query, document):
    query_words = tokenize(query)
    document_words = tokenize(document_text(document))

    if not query_words:
        return 0

    common_words = query_words.intersection(document_words)

    return len(common_words) / len(query_words)


def find_candidates(query, documents, top_k=5):
    scored_documents = []

    for document in documents:
        score = calculate_overlap(query, document)

        scored_documents.append(
            (score, document)
        )

    scored_documents.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return scored_documents[:top_k]


if __name__ == "__main__":
    print("=" * 60)
    print("GROUND TRUTH CANDIDATE SEARCH")
    print("=" * 60)

    documents = load_dataset()

    print(f"Total documents: {len(documents)}")

    for item in evaluation_queries:
        query = item["query"]

        candidates = find_candidates(
            query,
            documents
        )

        print("\n" + "-" * 60)
        print(f"Query: {query}")

        for rank, (score, document) in enumerate(
            candidates,
            start=1
        ):
            print(
                f"{rank}. "
                f"{document['document_id']} | "
                f"{document['title']} | "
                f"Score: {score:.3f}"
            )