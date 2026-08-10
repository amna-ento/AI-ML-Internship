from fastapi import FastAPI, HTTPException

from app.model_loader import load_model
from app.schemas import (
    HousePredictionRequest,
    HousePredictionResponse
)
from app.prediction_service import predict_price


app = FastAPI(
    title="House Price Prediction API",
    description="API for predicting house prices using Machine Learning",
    version="1.0.0"
)


# Load model when the application starts
model = load_model()


@app.get("/")
def root():
    return {
        "message": "House Price Prediction API"
    }


@app.get("/health")
def health():
    if model is None:
        return {
            "status": "unhealthy"
        }

    return {
        "status": "healthy"
    }


@app.post(
    "/predict",
    response_model=HousePredictionResponse
)
def predict(house: HousePredictionRequest):

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model file is not available"
        )

    try:
        result = predict_price(model, house)

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while making the prediction"
        )