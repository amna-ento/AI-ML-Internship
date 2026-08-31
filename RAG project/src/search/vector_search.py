import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_PATH = "data/chroma"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection("rag_chunks")


query = input("Enter your search query: ")

query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)


print("\n" + "=" * 60)
print("VECTOR SEARCH RESULTS")
print("=" * 60)

for i in range(len(results["ids"][0])):

    print(f"\nResult {i + 1}")
    print("-" * 60)

    print("Chunk ID:", results["ids"][0][i])
    print("Distance:", results["distances"][0][i])

    print("Content:")
    print(results["documents"][0][i][:500])