from fastapi import FastAPI
from app.models.schemas import ChatRequest, CreateUserRequest
from app.services.llm_service import run_assistant
from app.services.user_service import create_user
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Company Assistant API is running"}


@app.post("/users")
async def create_new_user(request: CreateUserRequest):
    user = create_user(
        request.name,
        request.email
    )

    return {
        "message": "User created successfully",
        "user": user
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    response = await run_assistant(
        request.message,
        request.user_id
    )

    return {"response": response}