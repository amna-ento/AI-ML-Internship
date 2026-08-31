import json


CHUNKS_PATH = "data/processed/chunks.json"


def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_content(chunk_ids):
    chunks = load_chunks()

    chunk_map = {
        chunk["chunk_id"]: chunk
        for chunk in chunks
    }

    results = []

    for chunk_id in chunk_ids:
        if chunk_id in chunk_map:
            results.append(chunk_map[chunk_id])

    return results


def build_context(chunks):
    context_parts = []

    for chunk in chunks:

        context = (
            f"[Document ID: {chunk['document_id']}]\n"
            f"Title: {chunk['title']}\n"
            f"Category: {chunk['category']}\n\n"
            f"{chunk['content']}"
        )

        context_parts.append(context)

    return "\n\n---\n\n".join(context_parts)


if __name__ == "__main__":

    print("=" * 60)
    print("CONTENT RETRIEVAL")
    print("=" * 60)

    chunks = load_chunks()

    print(f"Total chunks available: {len(chunks)}")

    test_ids = [
        chunks[0]["chunk_id"],
        chunks[1]["chunk_id"]
    ]

    results = retrieve_content(test_ids)

    print(f"\nRetrieved chunks: {len(results)}")

    context = build_context(results)

    print("\n" + "=" * 60)
    print("FINAL RAG CONTEXT")
    print("=" * 60)

    print(context)