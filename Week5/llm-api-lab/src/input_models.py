from pydantic import BaseModel, Field


class JobDescriptionInput(BaseModel):
    job_description: str = Field(
        min_length=1,
        max_length=2000
    )