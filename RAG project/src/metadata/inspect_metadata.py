import json

CHUNKS_PATH = "data/processed/chunks.json"


with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
    chunks = json.load(file)


print("=" * 60)
print("METADATA INSPECTION")
print("=" * 60)

print(f"\nTotal chunks: {len(chunks)}")

first_chunk = chunks[0]

print("\n--- First chunk ---")

for key, value in first_chunk.items():
    if key != "text":
        print(f"{key}: {value}")

print("\n--- Metadata fields ---")

metadata_fields = [
    "document_id",
    "title",
    "category",
    "subcategory",
    "department",
    "status",
    "language",
    "policy_type"
]

for field in metadata_fields:
    value = first_chunk.get(field)

    if value is not None:
        print(f"✓ {field}: {value}")
    else:
        print(f"✗ {field}: MISSING")