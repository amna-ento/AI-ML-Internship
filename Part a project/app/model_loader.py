import os
import joblib


MODEL_PATH = "models/house_price_model.pkl"


def load_model():
    if not os.path.exists(MODEL_PATH):
        return None

    return joblib.load(MODEL_PATH)


if __name__ == "__main__":
    model = load_model()

    if model is not None:
        print("Model loaded successfully")
        print(model)
    else:
        print("Model file is not available")