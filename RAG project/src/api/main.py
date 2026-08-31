from fastapi import FastAPI

from src.api.schemas import SearchRequest, SearchResponse
from src.retrieval.rag_retrieval import retrieve_for_api


app = FastAPI(
    title="RAG API",
    description="API for the RAG retrieval system",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "RAG API"
    }


@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):

    result = retrieve_for_api(
        request.query,
        request.top_k
    )

    return {
        "query": result["query"],
        "total_results": len(result["results"]),
        "results": result["results"],
        "context": result["context"]
    }