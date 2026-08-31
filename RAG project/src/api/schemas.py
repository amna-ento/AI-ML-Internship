from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
        description="User's search query"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of results to retrieve"
    )


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    title: str
    section: str
    content: str
    hybrid_score: float


class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: list[SearchResult]
    context: str