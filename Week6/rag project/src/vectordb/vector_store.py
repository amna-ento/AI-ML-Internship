from pathlib import Path

import chromadb


BASE_DIR = Path(__file__).resolve().parents[2]

CHROMA_PATH = BASE_DIR / "data" / "vector_db"

COLLECTION_NAME = "company_knowledge_base"


def get_chroma_client():
    """Create a persistent ChromaDB client."""

    return chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )


def get_collection():
    """Get or create the ChromaDB collection."""

    client = get_chroma_client()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "hnsw:space": "cosine"
        }
    )

    return collection


def add_chunks(chunks, embeddings):
    """Store chunks, embeddings, and metadata in ChromaDB."""

    collection = get_collection()

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:

        ids.append(chunk["chunk_id"])
        documents.append(chunk["text"])

        metadatas.append({
            "document_id": chunk["document_id"],
            "title": chunk["title"],
            "category": chunk["category"],
            "source": chunk["source"],
            "effective_date": chunk["effective_date"],
            "last_updated": chunk["last_updated"],
            "department": chunk["department"],
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
    )

    return len(ids)