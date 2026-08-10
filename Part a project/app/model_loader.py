import os
import joblib

MODEL_PATH = "models/house_price_model.pkl"


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model file not found")

    return joblib.load(MODEL_PATH)


if __name__ == "__main__":
    model = load_model()
    print("Model loaded successfully")
    print(model)
    
    
    