from pydantic import BaseModel


class HousePredictionRequest(BaseModel):
    area: float
    bedrooms: int
    bathrooms: int
    age: int
    location: str


class HousePredictionResponse(BaseModel):
    predicted_price: float
    mae: float
    r2_score: float | None