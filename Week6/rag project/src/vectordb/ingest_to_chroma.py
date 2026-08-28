from src.ingestion.loader import get_documents
from src.chunking.chunker import chunk_documents
from src.embedding.embedder import generate_embeddings
from src.vectordb.vector_store import add_chunks


def main():

    print("Loading documents...")
    documents = get_documents()

    print(f"Documents loaded: {len(documents)}")

    print("\nChunking documents...")
    chunks = chunk_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    print("\nGenerating embeddings...")
    texts = [chunk["text"] for chunk in chunks]

    embeddings = generate_embeddings(texts)

    print(f"Embeddings generated: {len(embeddings)}")
    print(f"Embedding dimensions: {len(embeddings[0])}")

    print("\nStoring chunks in ChromaDB...")
    count = add_chunks(chunks, embeddings)

    print(f"Chunks stored: {count}")

    print("\nIngestion completed successfully!")


if __name__ == "__main__":
    main()