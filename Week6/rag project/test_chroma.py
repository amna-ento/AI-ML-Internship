
from src.vectordb.vector_store import get_collection


collection = get_collection()

print("Total chunks:", collection.count())

results = collection.get(
    where={
        "$and": [
            {
                "category": "HR Policies"
            },
            {
                "source": "NexaCore HR Handbook"
            }
        ]
    },
    limit=10
)

print("\nFiltered chunks:", len(results["ids"]))

print("\nResults:")

for i in range(len(results["ids"])):
    metadata = results["metadatas"][i]

    print("\nID:", results["ids"][i])
    print("Title:", metadata["title"])
    print("Category:", metadata["category"])
    print("Source:", metadata["source"])
    print("Department:", metadata["department"])
