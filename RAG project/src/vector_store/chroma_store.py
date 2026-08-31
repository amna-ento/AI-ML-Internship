
import json
import chromadb


EMBEDDINGS_PATH = "data/processed/embeddings.json"
CHUNKS_PATH = "data/processed/chunks.json"

CHROMA_PATH = "data/chroma"
COLLECTION_NAME = "rag_chunks"


def load_embeddings():
    with open(EMBEDDINGS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def create_metadata_map(chunks):
    metadata_map = {}

    for chunk in chunks:
        metadata_map[chunk["chunk_id"]] = {
            "document_id": chunk["document_id"],
            "title": chunk["title"],
            "category": chunk["category"],
            "subcategory": chunk["subcategory"],
            "department": chunk["department"],
            "status": chunk["status"],
            "language": chunk["language"],
            "policy_type": chunk["policy_type"],
            "section": chunk["section"]
        }

    return metadata_map


def create_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    existing_collections = client.list_collections()

    collection_names = [collection.name for collection in existing_collections]

    if COLLECTION_NAME in collection_names:
        print("\nExisting collection found.")
        print("Deleting old collection...")
        client.delete_collection(COLLECTION_NAME)
        print("✓ Old collection deleted")

    collection = client.create_collection(
        name=COLLECTION_NAME
    )

    print("✓ New collection created")

    return collection


def add_embeddings(collection, embeddings, metadata_map):
    ids = []
    documents = []
    vectors = []
    metadatas = []

    for chunk in embeddings:
        chunk_id = chunk["chunk_id"]

        ids.append(chunk_id)
        documents.append(chunk["content"])
        vectors.append(chunk["embedding"])
        metadatas.append(metadata_map[chunk_id])

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=vectors,
        metadatas=metadatas
    )


def main():
    print("=" * 60)
    print("CHROMADB VECTOR STORE WITH METADATA")
    print("=" * 60)

    print("\nLoading embeddings...")
    embeddings = load_embeddings()
    print(f"Embeddings loaded: {len(embeddings)}")

    print("\nLoading chunks...")
    chunks = load_chunks()
    print(f"Chunks loaded: {len(chunks)}")

    print("\nCreating metadata map...")
    metadata_map = create_metadata_map(chunks)
    print(f"Metadata records created: {len(metadata_map)}")

    print("\nCreating ChromaDB collection...")
    collection = create_collection()
    print(f"Collection: {COLLECTION_NAME}")

    print("\nAdding embeddings, documents, and metadata...")

    add_embeddings(
        collection,
        embeddings,
        metadata_map
    )

    print("✓ Embeddings added")
    print("✓ Documents added")
    print("✓ Metadata added")

    print(f"\nVectors stored: {collection.count()}")

    print("\n✓ ChromaDB setup completed")


if __name__ == "__main__":
    main()
