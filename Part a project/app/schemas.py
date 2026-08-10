from pydantic import BaseModel, Field


class HousePredictionRequest(BaseModel):
    area_sqft: float = Field(gt=0)
    bedrooms: int = Field(gt=0)
    bathrooms: int = Field(gt=0)
    age_years: int = Field(ge=0)
    city: str = Field(min_length=1)
    location: str = Field(min_length=1)


class HousePredictionResponse(BaseModel):
    predicted_price: str
    mae: float
    r2_score: float