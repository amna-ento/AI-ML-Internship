from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_embedding_model():
    """Load the sentence-transformer embedding model."""

    return SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts):
    """Generate embeddings for a list of texts."""

    model = load_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings