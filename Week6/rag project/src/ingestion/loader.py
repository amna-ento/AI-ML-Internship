import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DOCUMENTS_PATH = BASE_DIR / "data" / "documents" / "company_policies.json"


def load_documents():
    """Load all company policy documents from JSON."""
    
    with open(DOCUMENTS_PATH, "r", encoding="utf-8") as file:
        documents = json.load(file)

    return documents


def validate_documents(documents):
    """Validate document count and required fields."""

    required_fields = {
        "document_id",
        "title",
        "category",
        "source",
        "effective_date",
        "last_updated",
        "department",
        "content",
    }

    if len(documents) != 250:
        raise ValueError(f"Expected 250 documents, found {len(documents)}")

    for document in documents:
        missing = required_fields - document.keys()

        if missing:
            raise ValueError(
                f"Document {document.get('document_id')} is missing: {missing}"
            )

    return True


def get_documents():
    """Load and validate all documents."""

    documents = load_documents()
    validate_documents(documents)

    return documents