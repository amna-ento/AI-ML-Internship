import pandas as pd

from app.schemas import HousePredictionRequest


VALID_LOCATIONS = {
    "lahore": "Lahore",
    "islamabad": "Islamabad"
}


def predict_price(model, house: HousePredictionRequest):

    location = house.location.strip().lower()

    if location not in VALID_LOCATIONS:
        raise ValueError(f"Unknown location: {house.location}")

    location = VALID_LOCATIONS[location]

    data = pd.DataFrame([{
        "area": house.area,
        "bedrooms": house.bedrooms,
        "bathrooms": house.bathrooms,
        "age": house.age,
        "location": location
    }])

    prediction = float(model.predict(data)[0])

    if prediction < 0:
        raise ValueError(
            "The model produced an invalid negative house price. "
            "Please provide realistic house details."
        )

    return prediction