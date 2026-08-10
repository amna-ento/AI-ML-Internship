
# House Price Prediction API

A simple Machine Learning and FastAPI project that predicts house prices based on house characteristics.

The project uses model trained on a house price dataset containing information about house area, bedrooms, bathrooms, age, city, and location.

The trained Machine Learning pipeline is saved using Joblib and loaded by the FastAPI application.

---

## Project Overview

The project has two main parts:

1. **Machine Learning**
   - Load and prepare the dataset
   - Check and clean the data
   - Select features and target
   - Encode categorical features
   - Split the dataset into training and testing data
   - Train and evaluate regression models
   - Save the trained model

2. **FastAPI**
   - Load the saved Machine Learning model
   - Validate user input
   - Accept house information
   - Predict the house price
   - Return the prediction and model evaluation metrics
   - Handle errors appropriately

---

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
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
│   └── house_data.csv
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

The new dataset contains **60 rows and 8 columns**.

The columns are:

```text
id
area_sqft
bedrooms
bathrooms
age_years
city
location
price
```

Example:

| id | area_sqft | bedrooms | bathrooms | age_years | city   | location    | price    |
|---:|----------:|---------:|----------:|----------:|--------|-------------|---------:|
| 1  | 3153      | 2        | 2         | 8         | Lahore | Bahria Town | 45358000 |
| 2  | 4356      | 2        | 2         | 2         | Lahore | DHA         | 58649000 |
| 3  | 2528      | 3        | 2         | 23        | Lahore | Wapda Town  | 40779000 |
| 4  | 4579      | 5        | 5         | 19        | Lahore | Johar Town  | 60391000 |
| 5  | 3687      | 3        | 4         | 9         | Lahore | Bahria Town | 54656000 |
```

---

## Loading the Dataset

The dataset is loaded using Pandas:

```python
import pandas as pd

df = pd.read_csv("house_data.csv")
```

---

## Data Checking and Cleaning

The dataset was checked for:

* Missing values
* Invalid values
* Duplicate rows
* Incorrect data types
* Invalid numerical values

The `id` column is used only as an identifier and is not used as a Machine Learning feature.

Therefore, it is removed before training:

```python
df = df.drop(columns=["id"])
```

---

## Features

The features used by the model are:

```text
area_sqft
bedrooms
bathrooms
age_years
city
location
```

These columns describe the characteristics of a house and can be used to predict its price.

---

## Target

The target variable is:

```text
price
```

The model learns the relationship between the house characteristics and its price.

---

# Data Preprocessing

There are two types of features in the dataset.

## Numerical Features

The following columns are numerical:

```text
area_sqft
bedrooms
bathrooms
age_years
```

These values are kept as numerical values.

## Categorical Features

The following columns contain categorical values:

```text
city
location
```

These columns are converted into numerical values using **One-Hot Encoding**.

The project uses a `ColumnTransformer` to apply the appropriate preprocessing to each type of feature.

The preprocessing and model are combined into a single Scikit-learn Pipeline:

```text
Numerical Features
        ↓
   Passthrough

City + Location
        ↓
One-Hot Encoding

        ↓

Linear Regression
```

This complete pipeline is saved as a single `.pkl` file.

---

# Train/Test Split

The dataset contains:

```text
60 rows
```

The data is divided into:

```text
80% Training
20% Testing
```

Therefore:

```text
Training samples = 48
Testing samples  = 12
```

The training data is used to train the model.

The testing data is kept separate and is used to evaluate how well the trained model performs on unseen data.

---

# Model Training

Three regression models were considered:

1. Linear Regression
2. Random Forest Regressor
3. Gradient Boosting Regressor

The models were compared using:

* MAE
* R² Score

Linear Regression was selected as the final model for this project.

The final pipeline contains:

```text
ColumnTransformer
        ↓
OneHotEncoder
        ↓
LinearRegression
```

---

# Model Evaluation

The final Linear Regression model was evaluated on the test dataset.


## MAE

**Mean Absolute Error (MAE)** measures the average difference between the actual house prices and the prices predicted by the model.

Our result:

```text
MAE = 2,480,529.53
```

This means that, on average, the model's predictions are approximately **2.48 million** away from the actual house prices in the test dataset.

## R² Score

**R² Score** measures how well the model explains the variation in house prices.

Our result:

```text
R² Score = 0.8849
```

This means that the model explains approximately **88.49%** of the variation in the test-set house prices.

---

# Model Persistence

After training and evaluation, the complete Machine Learning pipeline is saved using Joblib:

```text
models/house_price_model.pkl
```

The saved file contains:

```text
Preprocessing
     +
Linear Regression Model
```

The model does not need to be trained again when the FastAPI application starts.

---

# FastAPI

## API Endpoints

The application provides three main endpoints:

```text
GET  /
GET  /health
POST /predict
```

---

## `GET /`

Returns a basic message confirming that the API is running.

### Response

```json
{
  "message": "House Price Prediction API"
}
```

---

## `GET /health`

Checks whether the trained Machine Learning model is available.

### Response

```json
{
  "status": "healthy"
}
```

If the model file is not available, the application reports an unhealthy status.

---

## `POST /predict`

Predicts the price of a house using the trained Machine Learning model.

## Request

The new API accepts:

```json
{
  "area_sqft": 3153,
  "bedrooms": 2,
  "bathrooms": 2,
  "age_years": 8,
  "city": "Lahore",
  "location": "Bahria Town"
}
```

The API sends these values to the saved Machine Learning pipeline.

---
The exact predicted price changes depending on the house information provided by the user.

The MAE and R² values represent the overall performance of the trained model on the test dataset.

Therefore, they remain the same for different prediction requests using the same trained model.

---

### Readable Price Format

The predicted price is formatted into a human-readable format.

For example:

```text
24540000
```

is returned as:

```text
24.54 million
```

This makes large house prices easier to understand.

---

# Input Validation

The API validates incoming requests using Pydantic.

| Field       | Validation             |
| ----------- | ---------------------- |
| `area_sqft` | Must be greater than 0 |
| `bedrooms`  | Must be greater than 0 |
| `bathrooms` | Must be greater than 0 |
| `age_years` | Must be 0 or greater   |
| `city`      | Must not be empty      |
| `location`  | Must not be empty      |

For example:

```json
{
  "area_sqft": -100,
  "bedrooms": 0,
  "bathrooms": -1,
  "age_years": -5,
  "city": "",
  "location": ""
}
```

is rejected by Pydantic validation.

Invalid input results in:

```text
HTTP 422
```

---

# Unknown City and Location

The API validates the categorical values before making a prediction.

The model was trained using the cities and locations present in the training dataset.

If the API receives a city or location that was not present during training, the request is rejected with a meaningful error instead of allowing an invalid prediction.

For example:

```json
{
  "area_sqft": 3153,
  "bedrooms": 2,
  "bathrooms": 2,
  "age_years": 8,
  "city": "UnknownCity",
  "location": "Unknown Area"
}
```

The API returns an appropriate error such as:

```json
{
  "detail": "Unknown city or location"
}
```

with HTTP status:

```text
400
```

---

# Error Handling

The API handles the following situations:

| Situation                   | HTTP Status |
| --------------------------- | ----------: |
| Invalid input               |       `422` |
| Unknown city/location       |       `400` |
| Missing model file          |       `503` |
| Unexpected prediction error |       `500` |

This prevents the application from crashing and provides meaningful responses to the user.

---

# Model Loading

The trained model is loaded when the FastAPI application starts.

The model loader uses:

```python
import joblib

model = joblib.load("models/house_price_model.pkl")
```

The model is loaded once and kept in memory.

This is better than loading the model every time `/predict` is called because:

```text
FastAPI starts
      ↓
Load model once
      ↓
Keep model in memory
      ↓
Multiple prediction requests
      ↓
Use the same model
```

This improves performance and avoids unnecessary model loading.

---

# Installation

## 1. Navigate to the Project

From the terminal:

```bash
cd "Part a project"
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

From Swagger, the following endpoints can be tested:

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


The exact predicted price depends on the input values and the trained model.

---

# Application Flow

The complete Machine Learning and API flow is:

```text
House Price Dataset
        ↓
Data Checking and Cleaning
        ↓
Remove ID Column
        ↓
Feature Selection
        ↓
Separate Target
        ↓
Train/Test Split
        ↓
One-Hot Encoding
(city + location)
        ↓
Linear Regression
        ↓
Model Evaluation
        ↓
MAE + R²
        ↓
Save Complete Pipeline
        ↓
house_price_model.pkl
        ↓
FastAPI Starts
        ↓
Load Saved Model
        ↓
User Sends Request
        ↓
Pydantic Validation
        ↓
City/Location Validation
        ↓
Create DataFrame
        ↓
Saved ML Pipeline
        ↓
Prediction
        ↓
Format Price
        ↓
Return Prediction + MAE + R²
```

---

# Why Training and API Code Are Separate

Machine Learning training and API serving have different responsibilities.

## Machine Learning Side

The training process is responsible for:

```text
Dataset
   ↓
Data Preparation
   ↓
Preprocessing
   ↓
Train Model
   ↓
Evaluate Model
   ↓
Save Model
```

This work is performed in the Jupyter Notebook.

## FastAPI Side

The API is responsible for:

```text
Load Saved Model
       ↓
Receive User Input
       ↓
Validate Input
       ↓
Make Prediction
       ↓
Return Response
```

The API does not train the model again.

This separation makes the application simpler, faster, and easier to maintain.

---

# Model Serialization

The trained Scikit-learn pipeline is saved using Joblib.

Example:

```python
import joblib

joblib.dump(
    model,
    "models/house_price_model.pkl"
)
```

The FastAPI application loads the saved pipeline:

```python
import joblib

model = joblib.load(
    "models/house_price_model.pkl"
)
```

This allows FastAPI to use the already-trained model without repeating the training process.

---

# Requirements

The project dependencies are listed in:

```text
requirements.txt
```

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

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Project Files

### `app/main.py`

Contains:

* FastAPI application
* `/` endpoint
* `/health` endpoint
* `/predict` endpoint
* HTTP error handling
* Model initialization

---

### `app/model_loader.py`

Responsible for:

* Finding the saved model
* Loading the Joblib pipeline
* Handling a missing model file

---

### `app/prediction_service.py`

Responsible for:

* Preparing prediction input
* Sending input to the ML pipeline
* Generating the prediction
* Formatting the price
* Returning MAE and R²

---

### `app/schemas.py`

Contains the Pydantic request and response schemas.

It validates:

* Area
* Bedrooms
* Bathrooms
* Age
* City
* Location

---

### `data/house_data.csv`

Contains the new house price dataset.

The dataset contains:

```text
60 rows
8 columns
```

---

### `models/house_price_model.pkl`

Contains the trained Scikit-learn preprocessing and Linear Regression pipeline.

---

### `requirements.txt`

Contains the Python packages required to run the project.

---

### `README.md`

Contains project documentation, installation instructions, API usage, and project explanation.

---

### Final Submission

The final project contains:

```text
1. Source code
2. Dataset
3. Trained ML model
4. requirements.txt
5. README.md
```

---

## Conclusion

This project demonstrates how to combine a Machine Learning regression model with FastAPI to create a simple house price prediction API.

The Machine Learning pipeline:

```text
Dataset
   ↓
Preprocessing
   ↓
Linear Regression
   ↓
Evaluation
   ↓
Saved Pipeline
```

is created separately from the API.

The FastAPI application:

```text
Load Model
   ↓
Validate User Input
   ↓
Receive House Details
   ↓
Make Prediction
   ↓
Format Price
   ↓
Return JSON Response
```



The API returns a human-readable predicted price along with these overall model evaluation metrics.

```
```
