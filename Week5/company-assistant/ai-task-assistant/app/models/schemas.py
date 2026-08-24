from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    user_id: int = Field(gt=0)
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("message cannot be empty")

        return value



class CreateUserRequest(BaseModel):
    name: str
    email: str

    @field_validator("name", "email")
    @classmethod
    def validate_fields(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("field cannot be empty")

        return value

class CreateTaskRequest(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("title cannot be empty")

        return value


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime


class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    completed: bool
    created_at: datetime
    
    
    
    


