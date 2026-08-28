
# RAG-Based Company Policy / HR Handbook Chatbot

## Project Progress Report

---

## 1. Project Overview

### Project Title

**RAG-Based Company Policy / HR Handbook Chatbot**

### Project Objective

The goal of this project is to build a **Retrieval-Augmented Generation (RAG) chatbot** that can answer questions about company policies and HR information using a collection of **250 company policy documents**.

Instead of asking an LLM to answer questions purely from its own knowledge, the system retrieves relevant information from the company's internal knowledge base and then uses that information to generate an answer.

The overall pipeline is:

```text
Company Policy Documents
        ↓
Document Ingestion
        ↓
Text Chunking
        ↓
Embedding Generation
        ↓
Vector Database
        ↓
Semantic Retrieval
        ↓
Keyword Retrieval
        ↓
Hybrid Search
        ↓
Metadata Filtering
        ↓
Query Rewriting
        ↓
Context Selection
        ↓
LLM
        ↓
Final Answer
````

---

# 2. Original Project Requirements

The project was intended to demonstrate the major components of a production-style RAG system.

The main requirements were:

1. Ingest **200+ company documents**
2. Create meaningful text chunks
3. Generate embeddings
4. Store embeddings in a vector database
5. Store metadata alongside each chunk
6. Perform semantic/vector search
7. Implement keyword search
8. Implement hybrid search
9. Implement metadata filtering
10. Implement query rewriting
11. Build a search interface
12. Return ranked results with similarity scores
13. Compare keyword search and semantic search
14. Evaluate retrieval quality
15. Generate a 2D visualization of the embedding space
16. Build the final RAG answer-generation pipeline
17. Evaluate the complete system

---

# 3. Technology Stack

| Component       | Technology                                   |
| --------------- | -------------------------------------------- |
| Language        | Python                                       |
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2`     |
| Embedding Size  | 384 dimensions                               |
| Vector Database | ChromaDB                                     |
| Keyword Search  | BM25                                         |
| BM25 Library    | `rank_bm25`                                  |
| Chunking        | LangChain RecursiveCharacterTextSplitter     |
| LLM             | Planned/available through project LLM client |
| Data Format     | JSON                                         |
| Environment     | Python virtual environment                   |

---

# 4. Dataset

The project contains:

```text
250 documents
```

The documents are stored in:

```text
data/documents/company_policies.json
```

Each document contains metadata such as:

```text
document_id
title
category
source
effective_date
last_updated
department
content
```

Example:

```text
Document ID:
HR-002

Title:
Probation and Confirmation Policy

Category:
HR Policies

Source:
NexaCore HR Handbook

Department:
Human Resources
```

---

# 5. Dataset Validation

The dataset was validated to ensure that the expected number of documents exists.

Current result:

```text
Documents: 250
Unique IDs: 250
```

The content lengths are approximately:

```text
Minimum: 1528 characters
Maximum: 1581 characters
```

We also discovered an important data-quality problem during development.

Initially, many documents contained identical generic sections.

For example, the entire `Policy Rules` section was identical across all 250 documents.

This caused a serious retrieval problem because many chunks had exactly the same semantic content.

The dataset was subsequently regenerated so that:

```text
Total documents: 250
Unique contents: 250
Duplicated contents: 0
```

This was an important correction because duplicated document content can make retrieval evaluation misleading.

---

# 6. Project Structure

The current project structure is approximately:

```text
rag project/
│
├── main.py
├── prompt.md
├── readme.md
├── requirements.txt
│
├── .env
├── .gitignore
│
├── data/
│   ├── documents/
│   │   └── company_policies.json
│   │
│   └── vector_db/
│       ├── chroma.sqlite3
│       └── vector index files
│
├── src/
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── chunking/
│   │   └── chunker.py
│   │
│   ├── embedding/
│   │   └── embedder.py
│   │
│   ├── ingestion/
│   │   └── loader.py
│   │
│   ├── llm/
│   │   └── llm_client.py
│   │
│   ├── prompts/
│   │   └── prompt_template.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── utils/
│   │   └── helper.py
│   │
│   └── vectordb/
│       ├── vector_store.py
│       └── ingest_to_chroma.py
│
└── test files
    ├── test_chroma.py
    ├── test_chroma_embeddings.py
    ├── test_chroma_query.py
    ├── test_retriever.py
    ├── test_vector_search.py
    ├── test_keyword_search.py
    ├── test_hybrid_search.py
    └── test_manual_search.py
```

---

# 7. Phase-by-Phase Progress

## Phase 1 — Project Structure

### Status:  COMPLETE

The project structure was created with separate modules for:

* ingestion
* chunking
* embeddings
* vector database
* retrieval
* LLM
* prompts
* API

This provides a modular architecture instead of putting the entire RAG pipeline into one Python file.

---

# 8. Phase 2 — Virtual Environment

### Status:  COMPLETE

A Python virtual environment was created:

```text
.venv/
```

The project is being executed inside this environment.

---

# 9. Phase 3 — Dependencies

### Status:  COMPLETE

The required libraries were installed, including the libraries required for:

* embeddings
* chunking
* ChromaDB
* BM25
* LLM interaction

---

# 10. Phase 4 — Installation Verification

### Status:  COMPLETE

The environment and dependencies were tested successfully.

The embedding model can be loaded and used.

---

# 11. Phase 5 — 250 Original Documents

### Status:  COMPLETE

The project contains:

```text
250 company policy documents
```

The documents contain realistic metadata and policy content.

Example categories include:

```text
HR Policies
Leave & Attendance
Compensation & Benefits
Remote Work
Recruitment
Performance Management
IT & Security
Data Privacy
Training & Development
Workplace Safety
```

---

# 12. Phase 6 — Document Ingestion

### Status:  COMPLETE

The loader was implemented in:

```text
src/ingestion/loader.py
```

It:

1. Loads the JSON file
2. Checks that there are exactly 250 documents
3. Checks required fields
4. Returns validated documents

The validation expects:

```text
250 documents
```

and required fields such as:

```text
document_id
title
category
source
effective_date
last_updated
department
content
```

---

# 13. Phase 7 — Chunking

### Status:  COMPLETE

The project uses:

```text
RecursiveCharacterTextSplitter
```

Current configuration:

```text
Chunk size: 800
Chunk overlap: 120
```

The 250 documents produced:

```text
750 chunks
```

Therefore, on average:

```text
750 / 250 = 3 chunks per document
```

The chunk IDs contain the original document ID.

Example:

```text
HR-002_chunk_001
HR-002_chunk_002
```

This allows us to trace a retrieved chunk back to its original document.

---

# 14. Phase 8 — Embeddings

### Status:  COMPLETE

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Each chunk is converted into a numerical vector.

Embedding dimension:

```text
384
```

Embeddings are generated with:

```text
normalize_embeddings=True
```

Therefore, embeddings are normalized to approximately unit length.

Example:

```text
Embedding dimensions: 384
Norm: approximately 1.0
```

This allows cosine similarity to be used effectively.

---

# 15. Phase 9 — ChromaDB

### Status:  COMPLETE

ChromaDB is being used as the vector database.

Collection:

```text
company_knowledge_base
```

Current number of stored chunks:

```text
750
```

Each stored chunk contains:

```text
ID
Document text
Embedding
Metadata
```

The metadata includes:

```text
document_id
title
category
source
effective_date
last_updated
department
```

---

# 16. Phase 10 — Metadata

### Status:  COMPLETE

Metadata is stored alongside each chunk.

For example:

```text
document_id = HR-002
title = Probation and Confirmation Policy
category = HR Policies
source = NexaCore HR Handbook
department = Human Resources
effective_date = 2025-01-31
last_updated = 2025-06-30
```

This will later allow us to filter retrieval results.

For example:

```text
Only search HR Policies
```

or:

```text
Only search documents from a particular department
```

or:

```text
Only search recently updated documents
```

---

# 17. Phase 11 — Vector/Semantic Retrieval

### Status:  COMPLETE

Semantic retrieval has been implemented and tested.

Example query:

```text
What is the probation and confirmation policy?
```

The correct document:

```text
HR-002 — Probation and Confirmation Policy
```

is successfully retrieved.

Current result:

```text
Rank: 1
ID: HR-002_chunk_001
Title: Probation and Confirmation Policy
Distance: 0.259349942
```

The second result is also semantically relevant:

```text
PM-014 — Probation Review Policy
```

This demonstrates that semantic search can identify conceptually related documents.

---

# 18. Important Retrieval Debugging

### Status:  RESOLVED

We encountered a major issue where ChromaDB appeared to return unrelated documents with identical distances.

For example:

```text
Remote Security Policy
Reference Checks Policy
Offer Letters Policy
Workplace Inspection Policy
```

were appearing at the top even though the query was about probation.

The investigation revealed that many chunks contained identical text.

We verified this with a duplicate-content check.

Initially:

```text
Total chunks: 750
Unique texts: 252
```

One generic section appeared:

```text
250 times
```

This was causing the retrieval system to behave poorly.

After correcting the underlying documents:

```text
Total documents: 250
Unique contents: 250
Duplicated contents: 0
```

The vector retrieval now behaves correctly.

---

# 19. Manual Cosine Similarity Verification

### Status:  COMPLETE

We independently calculated cosine similarity to verify that ChromaDB was not the source of the problem.

For:

```text
Query:
What is the probation and confirmation policy?

Document:
HR-002_chunk_001
```

Manual cosine similarity:

```text
0.7406504824
```

Cosine distance:

```text
0.2593495176
```

ChromaDB produced approximately:

```text
0.259349942
```

The tiny difference is floating-point precision.

This confirmed that:

```text
Embedding generation 
Stored embedding 
ChromaDB distance calculation 
```

are working correctly.

---

# 20. Phase 12 — Keyword Search / BM25

### Status:  COMPLETE

BM25 keyword search has been implemented.

Example query:

```text
What is the probation and confirmation policy?
```

Result:

```text
Rank 1
HR-002 — Probation and Confirmation Policy
BM25 Score: 13.8273
```

Second:

```text
PM-014 — Probation Review Policy
BM25 Score: 12.6967
```

This demonstrates that keyword search can perform very well when the query contains exact terms from the document.

---

# 21. Phase 13 — Hybrid Search

### Status:  IMPLEMENTED, NEEDS FINAL VALIDATION

Hybrid search combines:

```text
Vector search
+
BM25 keyword search
```

The purpose is to obtain the strengths of both approaches.

Conceptually:

```text
Hybrid Score =
0.7 × Vector Score
+
0.3 × BM25 Score
```

The first implementation produced incorrect results because the vector-score normalization was not handling the retrieval scores correctly.

We identified this through testing.

Therefore, hybrid search exists, but it still needs to be **properly validated and finalized** before considering this phase completely finished.

---

# 22. Current Retrieval Architecture

The current retrieval architecture is:

```text
                 User Query
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
   Query Embedding           BM25
          │                     │
          ↓                     ↓
   Vector Search          Keyword Search
          │                     │
          └──────────┬──────────┘
                     ↓
               Hybrid Ranking
                     ↓
                 Top K
```

This is the foundation for the final RAG system.

---

# 23. What Has Been Successfully Verified

The following components have been directly tested:

```text
250 documents                    ✅
250 unique document IDs          ✅
250 unique document contents     ✅
750 chunks                       ✅
800 chunk size                   ✅
120 chunk overlap                ✅
384-dimensional embeddings       ✅
Normalized embeddings            ✅
ChromaDB collection              ✅
750 stored chunks                ✅
Metadata storage                 ✅
Vector retrieval                 ✅
Cosine similarity                ✅
BM25 keyword search              ✅
Manual retrieval verification    ✅
```

---

# 24. Remaining Work

The major remaining components are:

## Phase 14 — Metadata Filtering

### Status:  TODO

Implement filtering by:

```text
category
department
source
effective_date
last_updated
```

Example:

```text
Find probation policies
ONLY from HR Policies
```

---

# 25. Phase 15 — Query Rewriting

### Status:  TODO

The user might ask:

```text
How long do I have to wait before I'm confirmed?
```

The system should rewrite the query into something more useful for retrieval:

```text
employee probation period confirmation policy
```

This can improve retrieval when the user's wording does not match the wording used in the documents.

---

# 26. Phase 16 — Final Hybrid Retrieval Pipeline

### Status:  TODO

We need to finalize the retrieval pipeline:

```text
User Query
    ↓
Query Rewriting
    ↓
Metadata Filtering
    ↓
Vector Search
    +
BM25 Search
    ↓
Hybrid Ranking
    ↓
Top K
```

The final search interface should return:

```text
Rank
Document ID
Title
Category
Similarity/Hybrid Score
Text
Metadata
```

---

# 27. Phase 17 — RAG Generation

### Status:  TODO

After retrieval, the selected chunks need to be sent to the LLM.

The final pipeline will become:

```text
User Question
      ↓
Query Rewriting
      ↓
Retrieval
      ↓
Top K Documents
      ↓
Context
      ↓
Prompt
      ↓
LLM
      ↓
Final Answer
```

The LLM should answer using the retrieved company policy information rather than inventing information.

---

# 28. Phase 18 — Ground Truth Evaluation

### Status:  PARTIALLY COMPLETE

A ground-truth dataset has already been created for retrieval evaluation.

This allows us to answer questions such as:

```text
Did the retriever find the correct document?
```

and measure metrics such as:

```text
Recall@K
Precision@K
MRR
Hit Rate
```

The next step is to run the final evaluation after the retrieval pipeline is stable.

---

# 29. Phase 19 — Keyword vs Semantic Search Comparison

### Status:  TODO

The project requirement includes comparing keyword and semantic search on:

```text
15 queries
```

We will compare:

```text
BM25
vs
Vector Search
vs
Hybrid Search
```

For each query we can record:

```text
Query
Expected document
BM25 rank
Vector rank
Hybrid rank
Winner
```

This will demonstrate where each search strategy performs best.

---

# 30. Phase 20 — Embedding Visualization

### Status:  TODO

The project requires a 2D visualization of the embedding space.

The process will be:

```text
384-dimensional embeddings
          ↓
Dimensionality Reduction
          ↓
2D coordinates
          ↓
Plot
```

Possible dimensionality reduction techniques:

```text
PCA
t-SNE
UMAP
```

The points can then be:

```text
colored by category
```

This will visually demonstrate whether similar company policies cluster together.

---

# 31. Phase 21 — Final Search Interface

### Status:  TODO

A search interface will be created where a user can enter:

```text
What is the probation period?
```

and receive something like:

```text
Rank 1
Probation and Confirmation Policy
Score: 0.74

Rank 2
Probation Review Policy
Score: 0.59
```

The interface should expose the retrieved evidence rather than only returning an answer.

---

# 32. Phase 22 — Final RAG Chatbot

### Status:  TODO

The final system will allow users to ask questions such as:

```text
What is the probation policy?

How many days of leave can I take?

What is the remote work policy?

Who approves employee leave?

What are the rules for salary reviews?
```

The chatbot will:

```text
Question
   ↓
Query rewriting
   ↓
Metadata filtering
   ↓
Hybrid retrieval
   ↓
Top K context
   ↓
LLM
   ↓
Answer + supporting information
```

---

# 33. Important Lessons Learned So Far

## 1. Embedding dimensions must match

Our system uses:

```text
384 dimensions
```

for both query and document embeddings.

---

## 2. ChromaDB distance is not cosine similarity

For normalized embeddings:

```text
Cosine similarity ≈ 1 - cosine distance
```

For HR-002:

```text
Similarity ≈ 0.74065

Distance ≈ 0.25935
```

Therefore, a **lower ChromaDB distance is better**.

---

## 3. Data quality directly affects RAG quality

The biggest retrieval issue was not initially the embedding model or ChromaDB.

It was duplicated document content.

If many documents contain identical text:

```text
same text
same embedding
same distance
```

then the vector database cannot distinguish between those documents.

Therefore:

```text
Good RAG
=
Good retrieval algorithm
+
Good embeddings
+
Good chunking
+
Good data
```

---

## 4. Keyword and semantic search have different strengths

BM25 is strong when the query contains exact terms.

Semantic search is strong when the query expresses the same concept using different wording.

Hybrid search attempts to combine both strengths.

---

# 34. Current Project Status

Overall:

```text
                    STATUS

Project Setup             ██████████ 100%
Dataset                   ██████████ 100%
Ingestion                 ██████████ 100%
Chunking                  ██████████ 100%
Embeddings                ██████████ 100%
ChromaDB                  ██████████ 100%
Metadata                  ██████████ 100%
Vector Retrieval          ██████████ 100%
BM25 Search               ██████████ 100%
Hybrid Search             ███████░░░  70%
Metadata Filtering        ░░░░░░░░░░   0%
Query Rewriting           ░░░░░░░░░░   0%
RAG Generation            ░░░░░░░░░░   0%
Evaluation                ████░░░░░░  40%
15-query Comparison      ░░░░░░░░░░   0%
Embedding Visualization   ░░░░░░░░░░   0%
Final Interface           ░░░░░░░░░░   0%
```

The core retrieval infrastructure is now working.

---

# 35. Current Architecture

At this stage, the project can be represented as:

```text
                 ┌─────────────────────┐
                 │ 250 Policy Documents│
                 └──────────┬──────────┘
                            │
                            ↓
                    Document Loader
                            │
                            ↓
                       Chunking
                     800 / 120
                            │
                            ↓
                     750 Chunks
                            │
                ┌───────────┴───────────┐
                ↓                       ↓
          Embedding Model             BM25
                │                       │
                ↓                       ↓
          384-D Vectors          Keyword Index
                │                       │
                ↓                       ↓
             ChromaDB              BM25 Search
                │                       │
                └───────────┬───────────┘
                            ↓
                      Hybrid Search
                            │
                     [NEXT: Filtering]
                            │
                     Query Rewriting
                            │
                            ↓
                       Top K Context
                            │
                            ↓
                           LLM
                            │
                            ↓
                     Final RAG Answer
```

---

# 36. Immediate Next Steps

The recommended order from this point is:

```text
1. Fix/finalize Hybrid Search
              ↓
2. Metadata Filtering
              ↓
3. Query Rewriting
              ↓
4. Final Retrieval Pipeline
              ↓
5. RAG Generation
              ↓
6. Ground Truth Evaluation
              ↓
7. 15-query BM25 vs Vector vs Hybrid comparison
              ↓
8. 2D Embedding Visualization
              ↓
9. Search Interface
              ↓
10. Final README / Project Report
```

---

# 37. Final Assessment

The project has successfully completed the **core RAG data and retrieval foundation**.

The most important milestones achieved are:

```text
250 documents
        ↓
750 chunks
        ↓
384-D embeddings
        ↓
ChromaDB
        ↓
Semantic search
        ↓
BM25 search
        ↓
Retrieval verification
```

The system is therefore **past the basic RAG setup stage**.

The remaining work focuses primarily on making the retrieval system more intelligent and production-like:

```text
Metadata Filtering
        +
Query Rewriting
        +
Correct Hybrid Ranking
        +
LLM Generation
        +
Evaluation
        +
Visualization
        +
User Interface
```

Once these are completed, the project will represent a complete end-to-end **Company Policy / HR Handbook RAG chatbot** rather than only a vector-search prototype.

