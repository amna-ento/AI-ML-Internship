
import json
import re
from pathlib import Path


INPUT_FILE = Path("data/processed/documents.json")
OUTPUT_FILE = Path("data/processed/chunks.json")


def load_documents():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def split_into_sections(content):
    pattern = r"(?m)^## (.+)$"
    matches = list(re.finditer(pattern, content))

    sections = []

    for i, match in enumerate(matches):
        section_name = match.group(1).strip()
        start = match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(content)

        section_content = content[start:end].strip()

        if section_content:
            sections.append({
                "section": section_name,
                "content": section_content
            })

    return sections


def create_chunks(documents):
    chunks = []

    for document in documents:
        sections = split_into_sections(document["content"])

        for index, section in enumerate(sections, start=1):
            chunk = {
                "chunk_id": f"{document['document_id']}-chunk-{index:03d}",
                "document_id": document["document_id"],
                "title": document["title"],
                "category": document["category"],
                "subcategory": document["subcategory"],
                "department": document["department"],
                "status": document["status"],
                "language": document["language"],
                "policy_type": document["policy_type"],
                "section": section["section"],
                "content": section["content"]
            }

            chunks.append(chunk)

    return chunks


def save_chunks(chunks):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(chunks, file, indent=2, ensure_ascii=False)


def main():
    print("=" * 60)
    print("DOCUMENT CHUNKING")
    print("=" * 60)

    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    chunks = create_chunks(documents)

    print(f"Chunks created: {len(chunks)}")

    save_chunks(chunks)

    print(f"✓ Chunks saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()