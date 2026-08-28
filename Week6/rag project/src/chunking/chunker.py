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