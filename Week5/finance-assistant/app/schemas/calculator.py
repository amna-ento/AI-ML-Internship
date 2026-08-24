from pydantic import BaseModel, Field


class CalculateInput(BaseModel):
    expression: str = Field(
        description="A mathematical expression to calculate"
    )


class CalculateOutput(BaseModel):
    result: float