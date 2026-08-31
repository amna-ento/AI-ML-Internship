import json
from pathlib import Path

from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"
INPUT_FILE = Path("data/processed/chunks.json")
OUTPUT_FILE = Path("data/processed/embeddings.json")
BATCH_SIZE = 32


def load_chunks():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_embeddings(chunks, model):
    texts = [chunk["content"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True
    )

    return embeddings


def save_embeddings(chunks, embeddings):
    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        chunk_with_embedding = chunk.copy()
        chunk_with_embedding["embedding"] = embedding.tolist()
        embedded_chunks.append(chunk_with_embedding)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(embedded_chunks, file, ensure_ascii=False)


def main():
    print("=" * 60)
    print("DOCUMENT EMBEDDING PIPELINE")
    print("=" * 60)

    print(f"\nLoading chunks from: {INPUT_FILE}")

    chunks = load_chunks()

    print(f"Chunks loaded: {len(chunks)}")

    print(f"\nLoading embedding model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    print("\nGenerating embeddings...")

    embeddings = generate_embeddings(chunks, model)

    print("\nEmbedding generation completed.")

    print(f"Embedding matrix shape: {embeddings.shape}")

    save_embeddings(chunks, embeddings)

    print(f"\nEmbeddings saved to: {OUTPUT_FILE}")

    print("\nValidation:")
    print(f"Chunks: {len(chunks)}")
    print(f"Embeddings: {len(embeddings)}")
    print(f"Dimensions: {embeddings.shape[1]}")

    print("\n" + "=" * 60)
    print("EMBEDDING PIPELINE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()