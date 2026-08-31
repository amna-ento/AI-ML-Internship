import json
from pathlib import Path


RAW_FILE = Path("data/raw/company_policies_rag_10_10_FINAL(1).json")
PROCESSED_FILE = Path("data/processed/documents.json")

REQUIRED_FIELDS = [
    "document_id",
    "title",
    "content"
]


def load_documents():
    with open(RAW_FILE, "r", encoding="utf-8") as file:
        documents = json.load(file)

    return documents


def validate_documents(documents):
    errors = []
    document_ids = set()

    for index, document in enumerate(documents):

        for field in REQUIRED_FIELDS:
            if field not in document:
                errors.append(
                    f"Document {index}: missing '{field}'"
                )

            elif not document[field]:
                errors.append(
                    f"Document {index}: empty '{field}'"
                )

        document_id = document.get("document_id")

        if document_id:
            if document_id in document_ids:
                errors.append(
                    f"Duplicate document_id: {document_id}"
                )

            document_ids.add(document_id)

    return errors


def save_documents(documents):
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(PROCESSED_FILE, "w", encoding="utf-8") as file:
        json.dump(documents, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    documents = load_documents()

    print("=" * 60)
    print("DOCUMENT INGESTION")
    print("=" * 60)

    print(f"Total documents loaded: {len(documents)}")

    errors = validate_documents(documents)

    print("\nValidation results:")

    if errors:
        print(f"❌ Validation failed: {len(errors)} errors found")

        for error in errors:
            print(f" - {error}")

    else:
        print("✓ All documents passed validation")
        print("✓ Required fields are present")
        print("✓ No duplicate document IDs")
        print("✓ No empty required fields")

        save_documents(documents)

        print(f"\n✓ Processed documents saved to: {PROCESSED_FILE}")