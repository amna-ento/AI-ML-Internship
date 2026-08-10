import pandas as pd

from app.schemas import HousePredictionRequest


MODEL_MAE = 2480529.53
MODEL_R2 = 0.8849


def format_price(price: float) -> str:
    if price >= 1_000_000:
        return f"{price / 1_000_000:.2f} million"

    if price >= 1_000:
        return f"{price / 1_000:.2f} thousand"

    return f"{price:.2f}"


def predict_price(model, house: HousePredictionRequest):

    data = pd.DataFrame([{
        "area_sqft": house.area_sqft,
        "bedrooms": house.bedrooms,
        "bathrooms": house.bathrooms,
        "age_years": house.age_years,
        "city": house.city.strip(),
        "location": house.location.strip()
    }])

    prediction = float(model.predict(data)[0])

    if prediction < 0:
        raise ValueError(
            "The model produced an invalid negative house price. "
            "Please provide realistic house details."
        )

    return {
        "predicted_price": format_price(prediction),
        "mae": MODEL_MAE,
        "r2_score": MODEL_R2
    }