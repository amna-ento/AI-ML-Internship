from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.llm import run_finance_assistant, stream_finance_assistant


app = FastAPI(
    title="Personal Finance Assistant",
    description="AI-powered personal finance assistant with tool calling and MCP",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "personal-finance-assistant"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    return run_finance_assistant(request.message)


@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    def generate():
        for chunk in stream_finance_assistant(request.message):
            if "content" in chunk:
                yield chunk["content"]

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )