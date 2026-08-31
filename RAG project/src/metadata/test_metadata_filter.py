
import chromadb


CHROMA_PATH = "data/chroma"
COLLECTION_NAME = "rag_chunks"


def create_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    return collection


def main():
    print("=" * 60)
    print("CHROMADB METADATA FILTER TEST")
    print("=" * 60)

    collection = create_collection()

    print(f"\nTotal vectors: {collection.count()}")

    print("\nSearching for HR Policies...")

    results = collection.get(
        where={
            "category": "HR Policies"
        },
        limit=10
    )

    print(f"Results returned: {len(results['ids'])}")

    print("\n--- Retrieved chunks ---")

    for i in range(len(results["ids"])):
        print(f"\nResult {i + 1}")
        print(f"Chunk ID: {results['ids'][i]}")
        print(f"Document ID: {results['metadatas'][i]['document_id']}")
        print(f"Category: {results['metadatas'][i]['category']}")
        print(f"Department: {results['metadatas'][i]['department']}")
        print(f"Section: {results['metadatas'][i]['section']}")
        print(f"Content: {results['documents'][i][:150]}...")


if __name__ == "__main__":
    main()
