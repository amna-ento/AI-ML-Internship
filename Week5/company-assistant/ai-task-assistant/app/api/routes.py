from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest, CreateTaskRequest
from app.services.llm_service import run_assistant
from app.services.task_service import create_task, list_tasks
from app.tools.user_tools import get_user


router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):
    try:
        response = run_assistant(
            request.message,
            request.user_id,
        )

        return {
            "response": response
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


@router.get("/users/{user_id}")
def get_user_endpoint(user_id: int):
    user = get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.get("/users/{user_id}/tasks")
def get_tasks_endpoint(user_id: int):
    user = get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return list_tasks(user_id)


@router.post("/users/{user_id}/tasks", status_code=201)
def create_task_endpoint(
    user_id: int,
    request: CreateTaskRequest,
):
    user = get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return create_task(
        user_id,
        request.title,
    )