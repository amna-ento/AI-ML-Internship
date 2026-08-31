evaluation_queries = [
    {
        "id": 1,
        "query": "How do I update my employee information?",
        "expected_document": "HR-001",
        "type": "exact"
    },
    {
        "id": 2,
        "query": "Where can I change my emergency contact?",
        "expected_document": "HR-001",
        "type": "exact"
    },
    {
        "id": 3,
        "query": "What paperwork is needed to change my legal name?",
        "expected_document": "HR-001",
        "type": "exact"
    },
    {
        "id": 4,
        "query": "Can my manager modify my employee record?",
        "expected_document": "HR-001",
        "type": "exact"
    },
    {
        "id": 5,
        "query": "What is the company's leave policy?",
        "expected_document": "LA-001",
        "type": "general"
    },
    {
        "id": 6,
        "query": "How many days of leave can an employee take?",
        "expected_document": "LA-001",
        "type": "semantic"
    },
    {
        "id": 7,
        "query": "Am I allowed to work remotely?",
        "expected_document": "RW-001",
        "type": "semantic"
    },
    {
        "id": 8,
        "query": "What are the requirements for working from home?",
        "expected_document": "RW-001",
        "type": "semantic"
    },
    {
        "id": 9,
        "query": "What should I do if I think my account has been compromised?",
        "expected_document": "IT-013",
        "type": "scenario"
    },
    {
        "id": 10,
        "query": "How do I report a security incident?",
        "expected_document": "IT-011",
        "type": "procedural"
    },
    {
        "id": 11,
        "query": "How does the employee performance review process work?",
        "expected_document": "PM-004",
        "type": "procedural"
    },
    {
        "id": 12,
        "query": "How can I claim a business travel expense?",
        "expected_document": "TE-008",
        "type": "procedural"
    },
    {
        "id": 13,
        "query": "What should I do when my personal details change?",
        "expected_document": "HR-001",
        "type": "paraphrased"
    },
    {
        "id": 14,
        "query": "Who handles corrections to information that affects someone's salary?",
        "expected_document": "HR-001",
        "type": "semantic"
    },
    {
        "id": 15,
        "query": "What is the best programming language for machine learning?",
        "expected_document": None,
        "type": "irrelevant"
    }
]


if __name__ == "__main__":
    print("=" * 60)
    print("RAG RETRIEVAL EVALUATION QUERIES")
    print("=" * 60)

    print(f"Total queries: {len(evaluation_queries)}")

    for item in evaluation_queries:
        print(
            f"{item['id']:02d}. "
            f"{item['query']} "
            f"-> {item['expected_document']}"
        )