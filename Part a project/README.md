
# House Price Prediction API

## Project Overview

This project uses a Machine Learning regression model to predict house prices from:

- Area
- Bedrooms
- Bathrooms
- Age
- Location

The trained Machine Learning pipeline is saved using Joblib and loaded by a FastAPI application.

The API provides endpoints for:

- Checking whether the API is running
- Checking application health
- Predicting a house price

---

## Technologies

- Python
- Pandas
- NumPy
- Sklearn
- Joblib
- FastAPI
- Uvicorn
- Pydantic

---

## Project Structure

```text
house-price-api/
│
├── app/
│   ├── main.py
│   ├── model_loader.py
│   ├── prediction_service.py
│   └── schemas.py
│
├── data/
│   └── houses.csv
│
├── models/
│   └── house_price_model.pkl
│
├── requirements.txt
└── README.md
````

---

# Machine Learning

## Dataset

The provided dataset contains the following columns:

```text
area
bedrooms
bathrooms
age
location
price
```

The features used by the model are:

```text
area
bedrooms
bathrooms
age
location
```

The target variable is:

```text
price
```

---

## Data Preprocessing

The numerical features are kept as numerical values.

The `location` column is categorical, so One-Hot Encoding is used.


---

## Train/Test Split

The dataset is split into:

```text
80% Training
20% Testing
```

The training data is used to train the model, while the testing data is used to evaluate its performance on unseen data.

---

## Model Comparison

Three regression models were compared:

1. Linear Regression
2. Random Forest Regressor
3. Gradient Boosting Regressor

| Model             |       MAE | R² Score |
| ----------------- | --------: | -------: |
| Linear Regression | 446,818.2 |      NaN |
| Random Forest     | 1,524,000 |      NaN |
| Gradient Boosting | 3,752,957 |      NaN |

---

## Model Selection

Linear Regression was selected because it achieved the lowest MAE among the tested models.

The final saved pipeline contains:

```text
ColumnTransformer
        ↓
OneHotEncoder
        ↓
LinearRegression
```

---

## Note About R²

The provided dataset contains only 5 observations.

With an 80/20 split:

```text
Training samples = 4
Testing samples = 1
```

R² cannot be meaningfully calculated with only one test observation, so the R² value is `NaN`.

The project does not replace or fabricate an R² value.

---

# FastAPI

## API Endpoints

### `GET /`

Returns a basic API message.

#### Response

```json
{
  "message": "House Price Prediction API"
}
```

---

### `GET /health`

Checks whether the trained model is available.

#### Response

```json
{
  "status": "healthy"
}
```

If the model file is missing, the API returns HTTP `503`.

---

### `POST /predict`

Predicts the price of a house.

#### Request

```json
{
  "area": 1800,
  "bedrooms": 3,
  "bathrooms": 2,
  "age": 5,
  "location": "Lahore"
}
```

#### Response

```json
{
  "predicted_price": 12450000.0
}
```

The exact prediction depends on the trained model.

---

# Input Validation

The API validates incoming requests using Pydantic.

| Field       | Validation             |
| ----------- | ---------------------- |
| `area`      | Must be greater than 0 |
| `bedrooms`  | Must be greater than 0 |
| `bathrooms` | Must be greater than 0 |
| `age`       | Must be 0 or greater   |
| `location`  | Must not be empty      |

Invalid input results in HTTP `422`.

---

# Unknown Location

The training dataset contains:

```text
Lahore
Islamabad
```

If a user sends an unknown location such as:

```json
{
  "area": 1800,
  "bedrooms": 3,
  "bathrooms": 2,
  "age": 5,
  "location": "Multan"
}
```

the API returns HTTP `400`:

```json
{
  "detail": "Unknown location: Multan"
}
```

---

# Error Handling

The API handles the following cases:

| Situation                   | HTTP Status |
| --------------------------- | ----------: |
| Invalid input               |       `422` |
| Unknown location            |       `400` |
| Missing model file          |       `503` |
| Unexpected prediction error |       `500` |

---

# Installation

## 1. Clone or Download the Project

Navigate to the project directory:

```bash
cd house-price-api
```

---

## 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

---

## 3. Activate the Virtual Environment

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the API

Start the FastAPI application from the project root:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

From Swagger, you can test:

```text
GET  /
GET  /health
POST /predict
```

---

# Testing the API

## Test Root Endpoint

```bash
curl http://127.0.0.1:8000/
```

Expected response:

```json
{
  "message": "House Price Prediction API"
}
```

---

## Test Health Endpoint

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

## Test Prediction Endpoint

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
-H "Content-Type: application/json" \
-d '{
  "area": 1800,
  "bedrooms": 3,
  "bathrooms": 2,
  "age": 5,
  "location": "Lahore"
}'
```

Example response:

```json
{
  "predicted_price": 12450000.0
}
```

The exact prediction depends on the trained model.

---

# Application Flow

The complete Machine Learning and API flow is:

```text
Dataset
   ↓
Data Cleaning
   ↓
Feature Selection
   ↓
One-Hot Encoding
   ↓
Train/Test Split
   ↓
Model Training
   ↓
Model Evaluation
   ↓
Model Selection
   ↓
Save Pipeline using Joblib
   ↓
FastAPI Starts
   ↓
Load Saved Pipeline
   ↓
User Sends Prediction Request
   ↓
Pydantic Validation
   ↓
Location Validation
   ↓
Create DataFrame
   ↓
Saved Pipeline
   ↓
Prediction
   ↓
JSON Response
```

---

# Why Training and API Code Are Separate

Machine Learning training and API serving have different responsibilities.

The training process:

```text
Dataset
   ↓
Preprocessing
   ↓
Training
   ↓
Evaluation
   ↓
Save Model
```

is performed separately.

The FastAPI application only needs to:

```text
Load Saved Model
      ↓
Receive Input
      ↓
Make Prediction
      ↓
Return Response
```

This prevents the model from being retrained every time a user requests a prediction.

The trained model is loaded once when the FastAPI application starts and remains available in memory.

---

# Model Serialization

The trained Scikit-learn pipeline is saved using Joblib:

```python
import joblib

joblib.dump(model, "models/house_price_model.pkl")
```

The FastAPI application loads the saved pipeline:

```python
import joblib

model = joblib.load("models/house_price_model.pkl")
```

This allows the API to use the already-trained model without performing the training process again.

---

# Requirements

The project dependencies are listed in `requirements.txt`.

Example:

```text
pandas
numpy
scikit-learn
joblib
fastapi
uvicorn
pydantic
```

Install them with:

```bash
pip install -r requirements.txt
```

---

# Project Files

## `app/main.py`

Contains the FastAPI application and API endpoints.

## `app/model_loader.py`

Responsible for loading the saved Machine Learning model.

## `app/prediction_service.py`

Contains prediction-related logic.

## `app/schemas.py`

Contains Pydantic request and response schemas.

## `data/houses.csv`

Contains the house price dataset.

## `models/house_price_model.pkl`

Contains the trained Scikit-learn pipeline.

## `requirements.txt`

Contains the Python dependencies required to run the project.

---

# Final Submission

The final project contains:

```text
1. Source code
2. Dataset
3. Trained ML model
4. requirements.txt
5. README.md
```

---

# Conclusion

This project demonstrates how to combine a Machine Learning regression model with FastAPI to create a simple prediction API.

The Machine Learning pipeline handles preprocessing and prediction, while FastAPI handles request validation, API routing, error handling, and returning predictions as JSON responses.

```
```
