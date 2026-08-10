from pydantic import BaseModel, Field


class HousePredictionRequest(BaseModel):
    area: float = Field(gt=0)
    bedrooms: int = Field(gt=0)
    bathrooms: int = Field(gt=0)
    age: int = Field(ge=0)
    location: str = Field(min_length=1)


class HousePredictionResponse(BaseModel):
    predicted_price: float