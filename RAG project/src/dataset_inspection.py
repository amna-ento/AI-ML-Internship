import json
from pathlib import Path
from collections import Counter


DATA_PATH = Path("data/raw/company_policies_rag_10_10_FINAL(1).json")


with open(DATA_PATH, "r", encoding="utf-8") as file:
    documents = json.load(file)


print("=" * 60)
print("DATASET INSPECTION REPORT")
print("=" * 60)

print(f"\nTotal documents: {len(documents)}")


print("\n--- Document IDs ---")
print(documents[0]["document_id"])
print(documents[-1]["document_id"])


print("\n--- Fields in first document ---")
for field in documents[0]:
    print(field)


print("\n--- Categories ---")
category_counts = Counter(
    document["category"]
    for document in documents
)

for category, count in category_counts.items():
    print(f"{category}: {count}")


print("\n--- Departments ---")
department_counts = Counter(
    document["department"]
    for document in documents
)

for department, count in department_counts.items():
    print(f"{department}: {count}")


print("\n--- Status ---")
status_counts = Counter(
    document["status"]
    for document in documents
)

for status, count in status_counts.items():
    print(f"{status}: {count}")


print("\n--- Language ---")
language_counts = Counter(
    document["language"]
    for document in documents
)

for language, count in language_counts.items():
    print(f"{language}: {count}")


print("\n--- Content Length ---")

content_lengths = [
    len(document["content"])
    for document in documents
]

print(f"Minimum characters: {min(content_lengths)}")
print(f"Maximum characters: {max(content_lengths)}")
print(
    f"Average characters: "
    f"{sum(content_lengths) / len(content_lengths):.0f}"
)


print("\n--- Keywords ---")

keyword_counts = [
    len(document["keywords"])
    for document in documents
]

print(f"Minimum keywords: {min(keyword_counts)}")
print(f"Maximum keywords: {max(keyword_counts)}")
print(
    f"Average keywords: "
    f"{sum(keyword_counts) / len(keyword_counts):.1f}"
)


print("\n--- Common Questions ---")

question_counts = [
    len(document["common_questions"])
    for document in documents
]

print(f"Minimum questions: {min(question_counts)}")
print(f"Maximum questions: {max(question_counts)}")
print(
    f"Average questions: "
    f"{sum(question_counts) / len(question_counts):.1f}"
)


print("\n--- Duplicate Document IDs ---")

ids = [
    document["document_id"]
    for document in documents
]

duplicate_ids = [
    document_id
    for document_id, count in Counter(ids).items()
    if count > 1
]

if duplicate_ids:
    print("Duplicates found:", duplicate_ids)
else:
    print("No duplicate document IDs found.")


print("\n--- Missing Fields ---")

required_fields = [
    "document_id",
    "title",
    "category",
    "content",
    "keywords",
    "aliases",
    "topics",
    "entities",
    "common_questions",
]


for field in required_fields:
    missing = sum(
        1
        for document in documents
        if not document.get(field)
    )

    print(f"{field}: {missing} missing")


print("\n" + "=" * 60)
print("INSPECTION COMPLETE")
print("=" * 60)