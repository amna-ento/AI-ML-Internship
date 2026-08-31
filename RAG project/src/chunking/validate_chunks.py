import json
from pathlib import Path
from collections import Counter


CHUNKS_FILE = Path("data/processed/chunks.json")


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_chunks(chunks):
    errors = []

    chunk_ids = [chunk["chunk_id"] for chunk in chunks]
    duplicate_ids = [
        chunk_id
        for chunk_id, count in Counter(chunk_ids).items()
        if count > 1
    ]

    if duplicate_ids:
        errors.append(f"Duplicate chunk IDs: {duplicate_ids}")

    required_fields = [
        "chunk_id",
        "document_id",
        "title",
        "category",
        "subcategory",
        "department",
        "section",
        "content"
    ]

    for index, chunk in enumerate(chunks):
        for field in required_fields:
            if field not in chunk or not chunk[field]:
                errors.append(
                    f"Chunk {index} is missing field: {field}"
                )

    return errors


def main():
    print("=" * 60)
    print("CHUNK VALIDATION")
    print("=" * 60)

    chunks = load_chunks()

    print(f"Total chunks: {len(chunks)}")

    errors = validate_chunks(chunks)

    if errors:
        print("\nValidation errors:")
        for error in errors:
            print(f"✗ {error}")
    else:
        print("\nValidation results:")
        print("✓ All chunks passed validation")
        print("✓ No duplicate chunk IDs")
        print("✓ Required fields are present")
        print("✓ No empty required fields")


if __name__ == "__main__":
    main()