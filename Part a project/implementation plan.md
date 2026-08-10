# Implementation Plan

## Technologies

- Python
- Pandas
- NumPy
- SK Learn
- Joblib
- FastAPI
- Uvicorn
- Pydantic

## ML Implementation

### Data Preparation

- Load CSV using Pandas
- Check missing values
- Check invalid values and duplicates
- Clean the dataset
- Separate features and target

### Features

- `area`
- `bedrooms`
- `bathrooms`
- `age`
- `location`

### Target

- `price`

### Preprocessing

- Numerical columns: keep numerical
- `location`:  One hot Encoding
- Use `ColumnTransformer`

### Train/Test Split

- 80% training
- 20% testing

### Models

Train and compare:

1. Linear Regression
2. Random Forest Regressor
3. Gradient Boosting Regressor

### Evaluation

Use:

- MAE
- R² Score

Select the best performing model based on test results.

### Save model 

Save the complete preprocessing + model pipeline using Joblib:

`models/house_price_model.pkl`

## FastAPI Implementation

### `main`

- Create FastAPI application
- Load model during application startup
- Register routes

### `schemas`

Create Pydantic request schema:

- `area > 0`
- `bedrooms > 0`
- `bathrooms > 0`
- `location` must not be empty


### `prediction service`

- Validate location
- Convert request data to DataFrame
- Send data to the saved pipeline
- Generate prediction
- Return predicted price


##  Error 

Handle errors as:

- Invalid input: `422`
- Unknown location: `400`
- Missing model: `503`
- Unexpected prediction error: `500`

## Invalid input
- Negative area
- Zero bedrooms
- Negative bathrooms
- Negative age


## Folder structure


The project will use a simple layered architecture:

```text
house-price-api/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── model_loader.py
│   └── prediction_service.py
│
├── models/
│   └── house_price_model.pkl
│
├── data/
│   └── House Price Prediction.csv
│
├── requirements.txt
└── README.md