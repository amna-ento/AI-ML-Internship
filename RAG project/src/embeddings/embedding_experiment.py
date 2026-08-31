from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "all-MiniLM-L6-v2"


def main():
    model = SentenceTransformer(MODEL_NAME)

    texts = [
        "Employees must update their bank details.",
        "Staff members need to change their banking information.",
        "The company provides safety training to employees.",
    ]

    embeddings = model.encode(texts)

    similarity_matrix = cosine_similarity(embeddings)

    print("=" * 60)
    print("COSINE SIMILARITY EXPERIMENT")
    print("=" * 60)

    print("\nTexts:")

    for i, text in enumerate(texts):
        print(f"{i + 1}. {text}")

    print("\nSimilarity Matrix:")
    print(similarity_matrix)

    print("\nPairwise Similarities:")
    print(f"Text 1 vs Text 2: {similarity_matrix[0][1]:.4f}")
    print(f"Text 1 vs Text 3: {similarity_matrix[0][2]:.4f}")
    print(f"Text 2 vs Text 3: {similarity_matrix[1][2]:.4f}")


if __name__ == "__main__":
    main()