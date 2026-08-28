
# role 

u've to act as an expert ai engineer, who is known by his simplicity and perfection in work

# context

u have to make me have hands on experience and the clear concept for making the RAG syatem, u've to observe them and decide how to make specific learn in a professional way, i don't want the theory only but alos the code the logic each and everything

# example

if someone will ask me to get help for a topic: 
- i'll divide eveything in chunks, 
- give the plan with the learner so he can alos have a view 
- make the folder structure with the learner and for each chunk give the theory of it(the theory would not t=not too much dry and long passage to learn, but to the point small give the whole picture of the concept)
- tell if we use this or do this we'll get this output or it can make this thing possible
- then when i've to give code i'll not give comments inside the code after code will tell about taht part like what is it doing etc and when i've to give the code 
- i'll mention the file nam elike in this file u have to add it or replace whole code.

# input

You have to make RAG system like a smallest and easiest project, u have to make it in a way that u implement everything line by line and make me implement. suggest me the simplest RAG projects that would be beginner frindly and best for someone to learn about how to make rag system from all aspects.

and for the project let me give u a few tipis that must the project contain in it:
- Ingest 200+ documents 
- Generate and store embeddings in a vector database, with metadata
- A search interface returning ranked results with similarity scores
- Metadata filtering (by date, category, source)
- A side-by-side comparison with keyword search on 15 queries — where does each win?
- A 2D visualisation of the embedding space, clustered and coloured
- Written analysis: which queries did semantic search fail on, and why?

# output

the output would be like:
- discuss the simplest project ideas i'll choose one 
- then u have make me install all the dependencies required fr that project 
- make me create the folder(the folder structure must be simple and clean)
- the theory would not be to much dry and long passages it would be to the point things mentioned in theory 
- when u give code als tell me the output for this would be something like this if it is not like this then make me correct that


# task

u have to take an example project taht will implement all of these things u have to firstly make everything individually implement then combiningly make a complete project. i also want the practical implementation side by, at the end a complete RAG system has to be made so i wwant along with each topic implemnt each concept related in making a RAG system.

# constraints
- we'll be moving topic by topic each to be covered in one response
- u don't have to give to much theory 
- in bullets give eveything theory related 
- forperformong one task along with code must give the output like this kinda thing is what we're gonna get at the end then make me match if not correct then fix the problem then move nxt 
- i've did some work u have to just check that and move nxt, u do not need to do thoes tasks i've did earlier


# phases of work done

Phase 1  → Folder structure       
Phase 2  → Virtual environment    
Phase 3  → Dependencies          
Phase 4  → Verify installation    
Phase 5  → 250 original documents
Phase 6  → Document ingestion
Phase 7  → Chunking
Phase 8  → Embeddings
Phase 9  → ChromaDB
Phase 10 → Metadata
Phase 11 → Keyword search
Phase 12 → Vector search
Phase 13 → Hybrid search
Phase 14 → Query rewriting
Phase 15 → Content retrieval
Phase 16 → FastAPI endpoints
Phase 17 → 15-query comparison
Phase 18 → 2D embedding visualization

# task done already

i've did these things:
Phase 1  → Folder structure       
Phase 2  → Virtual environment    
Phase 3  → Dependencies           
Phase 4  → Verify installation   
Phase 5  → 250 original documents
Phase 6  → Document ingestion
Phase 7  → Chunking
Phase 8  → Embeddings


# code for required files
> loader.py
```
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DOCUMENTS_PATH = BASE_DIR / "data" / "documents" / "company_policies.json"


def load_documents():
    """Load all company policy documents from JSON."""
    
    with open(DOCUMENTS_PATH, "r", encoding="utf-8") as file:
        documents = json.load(file)

    return documents


def validate_documents(documents):
    """Validate document count and required fields."""

    required_fields = {
        "document_id",
        "title",
        "category",
        "source",
        "effective_date",
        "last_updated",
        "department",
        "content",
    }

    if len(documents) != 250:
        raise ValueError(f"Expected 250 documents, found {len(documents)}")

    for document in documents:
        missing = required_fields - document.keys()

        if missing:
            raise ValueError(
                f"Document {document.get('document_id')} is missing: {missing}"
            )

    return True


def get_documents():
    """Load and validate all documents."""

    documents = load_documents()
    validate_documents(documents)

    return documents
    ```

> chunker.py
```
from langchain_text_splitters import RecursiveCharacterTextSplitter


CHUNK_SIZE = 800
CHUNK_OVERLAP = 120


def create_splitter():
    """Create the recursive text splitter."""

    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ],
    )


def chunk_document(document):
    """Split one document into chunks."""

    splitter = create_splitter()

    texts = splitter.split_text(document["content"])

    chunks = []

    for index, text in enumerate(texts):

        chunks.append({
            "chunk_id": f"{document['document_id']}_chunk_{index + 1:03d}",
            "document_id": document["document_id"],
            "text": text,
            "title": document["title"],
            "category": document["category"],
            "source": document["source"],
            "effective_date": document["effective_date"],
            "last_updated": document["last_updated"],
            "department": document["department"],
        })

    return chunks


def chunk_documents(documents):
    """Chunk all documents."""

    all_chunks = []

    for document in documents:
        chunks = chunk_document(document)
        all_chunks.extend(chunks)

    return all_chunks
    ```

> embedder.py
```
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
```

