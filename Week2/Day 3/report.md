# Stock Price Prediction Project Report

# 1. Problem Statement

<<<<<<< HEAD
The stock market is dynamic, making future stock price prediction a challenging regression problem. In this project, historical **New York Stock Exchange (NYSE)** data was used to predict the **next day's closing stock price**. Multiple regression models were compared to identify the most accurate one.
=======

>>>>>>> dfbcfc3bb7c9a7a4747362e2d1b5dfe74f9e24ae

---

# 2. Project Goal

The main objective of this project was to develop a machine learning regression model that predicts the **next day's closing stock price** using historical trading information.

### Project Goals

- Predict tomorrow's closing stock price.
- Compare multiple regression algorithms.
- Identify the best-performing model based on prediction accuracy.

<<<<<<< HEAD
=======

>>>>>>> dfbcfc3bb7c9a7a4747362e2d1b5dfe74f9e24ae

---

# 3. Dataset Overview

<<<<<<< HEAD
## Dataset Source

The dataset was obtained from the **New York Stock Exchange (NYSE) historical stock market dataset**.

**Dataset link:** https://www.kaggle.com/datasets/dgawlik/nyse?select=prices-split-adjusted.csv

## Dataset Description

The dataset contains historical daily stock prices of companies listed on the NYSE. Split-adjusted prices were used to ensure that historical stock prices remained consistent after stock splits.

### Data Used for This Project

For this project, only the historical records of **Apple Inc. (AAPL)** were selected.

## Features in the Dataset

| Feature | Description |
|----------|-------------|
| Date | Trading date |
| Symbol | Company stock symbol |
| Open | Opening stock price |
| Close | Closing stock price |
| Low | Lowest stock price during the day |
| High | Highest stock price during the day |
| Volume | Number of shares traded |

## Data Characteristics

- Historical daily stock prices
- Time-series dataset
- Numerical and date features
- Suitable for regression-based forecasting
=======

- Dataset source
- Number of rows and columns
- Type of data
- Important characteristics]
>>>>>>> dfbcfc3bb7c9a7a4747362e2d1b5dfe74f9e24ae

---

# 4. Why This Dataset Was Chosen

This dataset was selected because it provides real-world historical stock market data suitable for regression analysis.

### Reasons for Choosing This Dataset

- Contains multiple years of historical stock prices.
- Represents a real financial forecasting problem.
- Provides continuous numerical values required for regression.

<<<<<<< HEAD
=======

>>>>>>> dfbcfc3bb7c9a7a4747362e2d1b5dfe74f9e24ae

---

# 5. Features Used

<<<<<<< HEAD
The following input features were used to predict the next day's closing stock price.

| Feature | Description |
|----------|-------------|
| Open | Opening stock price of the current trading day |
| High | Highest stock price reached during the day |
| Low | Lowest stock price reached during the day |
| Close | Closing stock price of the current day |
| Volume | Number of shares traded during the day |

## Why These Features Were Selected

- **Open Price:** Indicates the market's starting price for the day.
- **High Price:** Shows the highest buying activity during the day.
- **Low Price:** Represents the lowest trading price.
- **Close Price:** Usually contains the strongest information about market movement.
- **Volume:** Reflects investor activity and market interest.

These features collectively provide sufficient information to estimate the stock price movement for the following trading day.
=======

- Feature 1: Description
- Feature 2: Description
>>>>>>> dfbcfc3bb7c9a7a4747362e2d1b5dfe74f9e24ae

---

# 6. Target Variable

<<<<<<< HEAD
The target variable for this project was:

**Tomorrow_Close**

This target was created by shifting the **Close** column one day upward.

### Example

| Today Close | Tomorrow Close (Target) |
|-------------|-------------------------|
| 30.57 | 30.63 |
| 30.63 | 30.14 |
| 30.14 | 30.08 |

This transformation allows the model to learn the relationship between today's market information and tomorrow's closing stock price.

## Why a New Target Was Created

The original dataset contains only the current day's stock prices. Since the project's objective was to predict the next day's closing price, a new target variable was created using:

```python
df["Tomorrow_Close"] = df["close"].shift(-1)
```

After shifting, the last row contained no target value because there is no next trading day available. Therefore, the last row was removed from the dataset before training the models.
=======

- Target: Tomorrow's Closing Stock Price
>>>>>>> dfbcfc3bb7c9a7a4747362e2d1b5dfe74f9e24ae


# 7. Data Inspection

Before training the machine learning models, the dataset was carefully inspected to understand its structure, quality, and overall condition. This process helps identify issues such as missing values, duplicate records, incorrect data types, and data inconsistencies that could affect model performance.

<<<<<<< HEAD

## Dataset Shape

The dataset contained historical daily stock prices with the following columns:

- Date
- Symbol
- Open
- Close
- Low
- High
- Volume

Only records belonging to **Apple Inc. (AAPL)** were selected for this project.

## Data Types

| Data Type | Columns |
|-----------|---------|
| Datetime | Date |
| Object | Symbol |
| Float | Open, Close, Low, High, Volume |

The **Date** column was converted into a proper datetime format to support chronological analysis.

## Missing Values

- No significant missing values were found in the selected Apple stock data.

## Duplicate Values


- No duplicate records were found.

## Statistical Summary


| Statistic | Open | Close | Low | High | Volume |
|-----------|------:|------:|-----:|------:|--------:|
| Count | 851,264 | 851,264 | 851,264 | 851,264 | 851,264 |
| Mean | 64.99 | 65.01 | 64.34 | 65.64 | 5.42M |
| Std Dev | 75.20 | 75.20 | 74.46 | 75.91 | 12.49M |
| Min | 1.66 | 1.59 | 1.50 | 1.81 | 0 |
| 25% | 31.27 | 31.29 | 30.94 | 31.62 | 1.22M |
| Median (50%) | 48.46 | 48.48 | 47.97 | 48.96 | 2.48M |
| 75% | 75.12 | 75.14 | 74.40 | 75.85 | 5.22M |
| Max | 1584.44 | 1578.13 | 1549.94 | 1600.93 | 859.64M |

These statistics helped understand the distribution and range of stock prices before model training.
=======
- Shape of dataset
- Data types
- Missing values
- Duplicate values
- Statistical summary]
>>>>>>> dfbcfc3bb7c9a7a4747362e2d1b5dfe74f9e24ae

---

# 8. Data Preprocessing Steps

After inspecting the dataset, several preprocessing steps were performed to prepare the data for machine learning.

## Step 1: Selected Apple Stock Data

The original dataset contains stock prices for multiple companies. Since this project focuses on Apple Inc., only **AAPL** records were selected.

### Reason

- Keeps the project focused on a single company.
- Prevents data from different companies from affecting the model.

---

## Step 4: Created the Target Variable

A new target column named **Tomorrow_Close** was created.

```python
df["Tomorrow_Close"] = df["close"].shift(-1)
```

### Reason

The objective of the project is to predict tomorrow's closing stock price rather than today's closing price.

---

## Step 5: Selected Features

The following input features were used:

- Open
- High
- Low
- Close
- Volume

### Reason

These variables directly influence daily stock price movements and provide useful information for predicting the next day's closing price.

---

## Step 6: Created Feature Matrix and Target Variable

The dataset was divided into:

### Features (X)

- Open
- High
- Low
- Close
- Volume

### Target (y)

- Tomorrow_Close

Separating the input features and target variable is required before training machine learning models.

---

# 9. Difficulties Found

Several challenges were encountered while working with the stock market dataset.

## Challenge 1: Time-Series Data

Unlike traditional datasets, stock market data is sequential and depends on time.

Future prices must never be used to predict past prices.

---

## Challenge 2: Creating the Prediction Target

The original dataset did not contain tomorrow's closing price.

A new target variable had to be created.

---

## Challenge 3: Data Leakage

Using a random train-test split could allow future stock prices to appear in the training data.

This would produce unrealistically high prediction accuracy.

---

## Challenge 4: Choosing the Correct Validation Method

Standard K-Fold Cross Validation randomly shuffles the data.

---

## Challenge 5: Model Selection

It was not known beforehand which regression algorithm would provide the best prediction performance.

Multiple models had to be trained and compared.

---

# 10. How Each Challenge Was Solved

## Challenge 1

### Problem

Time-series data must remain in chronological order.

### Solution

The dataset was sorted by date, and chronological splitting was used instead of random shuffling.

---

## Challenge 2

### Problem

The dataset did not contain tomorrow's closing price.

### Solution

A new target variable was created using:

```python
df["Tomorrow_Close"] = df["close"].shift(-1)
```

---

## Challenge 3

### Problem

Random splitting could introduce data leakage.

### Solution

The dataset was split using time-based ordering (`shuffle=False`), ensuring that training data always came before testing data.

---

## Challenge 4

### Problem

Traditional K-Fold Cross Validation is not suitable for time-series datasets.

### Solution

`TimeSeriesSplit` was used because it preserves chronological order and evaluates the model using only future observations.

---

## Challenge 5

### Problem

The best-performing regression model was unknown.

### Solution

Four regression models were trained and compared:

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor

Their performance was evaluated using:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

---

# 11. Feature Engineering

Feature engineering improves the dataset by creating variables that help the machine learning model learn useful patterns.

## Target Variable Creation

The primary engineered feature in this project was:

**Tomorrow_Close**

```python
df["Tomorrow_Close"] = df["close"].shift(-1)
```

This shifts the closing price one day upward, allowing the model to learn the relationship between today's market values and tomorrow's closing price.

## Input Features

The following features were retained:

- Open
- High
- Low
- Close
- Volume

---

# 12. Train/Test Splitting (Time Series)

The dataset was divided into training and testing sets using a chronological (time-based) split.

## Why Random Splitting Was Avoided

Randomly shuffling stock market data would allow the model to learn from future observations, resulting in data leakage and unrealistically high evaluation scores.

## Time-Based Splitting Approach

The data was divided chronologically:

- **Training Set:** Earlier trading records
- **Testing Set:** Most recent trading records

This approach simulates real-world forecasting, where a model is trained on historical data and then used to predict future stock prices.

## Benefits of Time-Based Splitting

- Preserves chronological order.
- Produces realistic model evaluation.
- Reflects real-world stock market prediction scenarios.

The `shuffle=False` parameter was used during the train-test split to maintain the natural sequence of the data.


# 13. Feature Scaling 

Feature scaling is the process of transforming numerical features so that they have a similar range of values. This helps certain machine learning algorithms learn more efficiently and prevents features with larger numerical values from dominating the learning process.

## Was Feature Scaling Applied?

Yes. Feature scaling was applied using **StandardScaler**.

The following features were scaled:

- Open
- High
- Low
- Close
- Volume

Scaling was performed **after splitting the dataset into training and testing sets** to prevent data leakage.

## Why Was Scaling Applied?

The selected features have very different numerical ranges.

For example:

- Stock prices range from approximately **30 to 130 USD**.
- Trading volume ranges from **millions to hundreds of millions of shares**.

Without scaling, features with larger values (such as **Volume**) could dominate the learning process, especially for algorithms that rely on numerical optimization.

## Which Models Required Scaling?

| Model | Scaling Required | Reason |
|--------|:---------------:|--------|
| Linear Regression | Yes | Coefficient estimation can be influenced by differences in feature scales. |
| Decision Tree Regressor | No | Tree splitting depends on feature thresholds rather than feature scale. |
| Random Forest Regressor | No | Ensemble of decision trees; scaling has little impact. |
| Gradient Boosting Regressor | No | Tree-based algorithm that is generally unaffected by feature scaling. |

---

# 14. Models Trained

To identify the most suitable algorithm for predicting tomorrow's stock price, four regression models were trained and evaluated.

---

## 14.1 Linear Regression

### Model Explanation

Linear Regression is one of the simplest and most widely used regression algorithms. It predicts the target variable by finding the best-fitting linear relationship between the input features and the target variable.

It assumes that changes in the input variables have a linear relationship with changes in the target.

### Why It Was Selected

- Easy to understand and implement.
- Fast training time.
- Provides a strong baseline for comparison.
- Performs well when relationships between variables are approximately linear.

### Results

| Metric | Value |
|--------|------:|
| MAE | 1.2193 |
| MSE | 2.9518 |
| RMSE | 1.7181 |
| R² Score | 0.9536 |

### Interpretation

Linear Regression achieved the **highest R² Score** and the **lowest prediction errors** among all models, making it the best-performing model for this project.


![Image Description](a.png)
*description*

---

## 14.2 Decision Tree Regressor

### Model Explanation

Decision Tree Regression predicts values by repeatedly splitting the dataset into smaller groups based on feature values.

Each split reduces prediction error until the model reaches a final prediction.

### Why It Was Selected

- Easy to interpret.
- Can model non-linear relationships.
- Does not require feature scaling.

### Results

| Metric | Value |
|--------|------:|
| MAE | 1.8932 |
| MSE | 5.7982 |
| RMSE | 2.4079 |
| R² Score | 0.9089 |

### Interpretation

The Decision Tree model captured non-linear relationships but produced larger prediction errors compared to the other models, indicating lower generalization performance.

![Image Description](b.png)

This graph shows the actual and predicted stock prices using the Decision Tree model. The predicted line follows the overall trend but has more noticeable differences, making it less accurate than the other models.

---

## 14.3 Random Forest Regressor

### Model Explanation

Random Forest is an ensemble learning algorithm that combines predictions from multiple decision trees to improve accuracy and reduce overfitting.

Each decision tree is trained using a random subset of the data and input features.

### Why It Was Selected

- Reduces overfitting compared to a single decision tree.
- Produces stable predictions.
- Handles complex non-linear relationships effectively.
- Provides feature importance analysis.

### Results

| Metric | Value |
|--------|------:|
| MAE | 1.4081 |
| MSE | 3.5918 |
| RMSE | 1.8952 |
| R² Score | 0.9436 |

### Interpretation

Random Forest achieved strong predictive performance with low prediction errors and excellent generalization capability.

![Image Description](c.png)

This graph compares the actual prices with the Random Forest predictions. The two lines are very close to each other, showing that the model predicts stock prices with high accuracy.

---

## 14.4 Gradient Boosting Regressor

### Model Explanation

Gradient Boosting is an ensemble learning algorithm that builds decision trees sequentially.

Each new tree learns from the errors made by the previous trees, gradually improving the model's prediction accuracy.

### Why It Was Selected

- Excellent predictive performance.
- Handles complex relationships effectively.
- Reduces prediction errors through sequential learning.

### Results

| Metric | Value |
|--------|------:|
| MAE | 1.4364 |
| MSE | 3.6481 |
| RMSE | 1.9100 |
| R² Score | 0.9427 |

### Interpretation

Gradient Boosting produced highly accurate predictions and performed similarly to Random Forest. However, its overall performance was slightly lower than Linear Regression on this dataset.

![Image Description](d.png)


This graph shows the predictions made by the Gradient Boosting model compared with the actual prices. The close overlap between the two lines indicates that the model captures the stock price trend effectively.


---

# 15. Evaluation Metrics Used

To evaluate the prediction performance of each regression model, four standard regression metrics were used.

---

## 15.1 Mean Absolute Error (MAE)

### Definition

Mean Absolute Error (MAE) measures the average absolute difference between the predicted values and the actual values.



- Measures the average prediction error.
- Lower MAE indicates better performance.
- Expressed in the same unit as the target variable.



---

## 15.2 Mean Squared Error (MSE)

### Definition

Mean Squared Error (MSE) calculates the average squared difference between the actual and predicted values.


### Interpretation

- Penalizes larger prediction errors more heavily.
- Lower MSE indicates better model performance.

---

## 15.3 Root Mean Squared Error (RMSE)

### Definition

Root Mean Squared Error (RMSE) is the square root of the Mean Squared Error.


### Interpretation

- Measures prediction error in the original unit of the target variable.
- Lower RMSE indicates higher prediction accuracy.
- More sensitive to large prediction errors than MAE.

---

## 15.4 R² Score (Coefficient of Determination)

### Definition

The R² Score measures how well the regression model explains the variation in the target variable.


### Interpretation

- R² ranges from negative values to **1**.
- A value closer to **1** indicates better predictive performance.
- Higher R² means the model explains a larger proportion of the variation in stock prices.

![Image Description](e.png)


This chart compares how well each model predicts stock prices. A higher R² score means better prediction accuracy, and Linear Regression achieved the highest score in this project.

---

# 16. Model Comparison Table

| Model | MAE | MSE | RMSE | R² Score |
|--------|----:|----:|-----:|---------:|
| Linear Regression | 1.2193 | 2.9518 | 1.7181 | 0.9536 |
| Decision Tree Regressor | 1.8932 | 5.7982 | 2.4079 | 0.9089 |
| Random Forest Regressor | 1.4081 | 3.5918 | 1.8952 | 0.9436 |
| Gradient Boosting Regressor | 1.4364 | 3.6481 | 1.9100 | 0.9427 |

## Comparison Summary

- **Linear Regression** achieved the highest **R² Score** and the lowest prediction errors, making it the best-performing model.
- **Random Forest Regressor** ranked second with strong predictive performance and good generalization.
- **Gradient Boosting Regressor** produced results very similar to Random Forest, with only slightly lower performance.
- **Decision Tree Regressor** had the largest prediction errors and the lowest R² Score among the four evaluated models.


# 17. Cross-Validation (TimeSeriesSplit)

Cross-validation was performed to evaluate how well the trained models generalize to unseen data. Instead of relying on a single train-test split, the models were validated using multiple chronological splits of the dataset.

## Why Cross-Validation Was Used

Using only one train-test split may produce results that depend on a particular division of the data. Cross-validation provides a more reliable estimate of model performance by evaluating the model on multiple subsets of the dataset.

### Benefits of Cross-Validation

- Provides a more reliable evaluation of model performance.
- Reduces the chance of misleading results from a single train-test split.
- Measures how consistently the model performs across different time periods.
- Helps compare different machine learning models fairly.

## Why TimeSeriesSplit Was Selected Instead of Normal K-Fold

The dataset used in this project is a **time-series dataset**, where observations are ordered chronologically by date.

A standard **K-Fold Cross Validation** randomly divides the dataset into folds. This may allow future observations to appear in the training set while earlier observations appear in the testing set, leading to **data leakage**.

To avoid this problem, **TimeSeriesSplit** was used.

TimeSeriesSplit preserves the chronological order of the data by training the model on earlier observations and validating it on later observations.


## Validation Results

TimeSeriesSplit was applied to all four regression models.

The validation results showed that:

- Linear Regression consistently achieved high prediction accuracy.
- Random Forest and Gradient Boosting also performed well but showed slightly higher prediction errors.
- Decision Tree exhibited greater variation across validation folds, indicating lower stability.

The cross-validation results confirmed that **Linear Regression** generalized well to unseen data, making it the most reliable model for this project.

---

# 18. Overfitting vs. Underfitting Analysis

One of the primary objectives of this project was to ensure that the trained models generalized well to unseen stock market data.

## Overfitting

Overfitting occurs when a model memorizes the training data instead of learning general patterns.

### Characteristics of an Overfitted Model

- Very high training accuracy.
- Lower testing performance.
- Poor generalization to unseen data.

Tree-based models such as **Decision Tree Regressor** are more likely to overfit if they are allowed to grow without restrictions.

## Underfitting

Underfitting occurs when a model is too simple to capture the underlying relationship between the input features and the target variable.

### Characteristics of an Underfitted Model

- High training error.
- High testing error.
- Poor prediction accuracy.

## Analysis of the Trained Models

The models were evaluated using both training and testing datasets.

### Observations

- Linear Regression showed excellent performance on both training and testing data, indicating strong generalization.
- Random Forest achieved high prediction accuracy while reducing the overfitting commonly seen in a single Decision Tree.
- Gradient Boosting also generalized well and produced stable predictions.
- Decision Tree showed comparatively lower testing performance, suggesting that it captured some dataset-specific patterns.

## How Overfitting Was Handled

The following techniques helped reduce overfitting:

- Used a chronological train-test split.
- Applied TimeSeriesSplit for model validation.
- Compared multiple machine learning models instead of relying on a single algorithm.
- Evaluated models using multiple regression metrics rather than a single performance measure.

These techniques ensured that the selected model performed well on both training data and previously unseen stock market data.

---

# 19. Feature Importance / Coefficients

Understanding which features contribute most to stock price prediction helps interpret the model and provides valuable insights into the factors influencing future prices.

## Linear Regression Coefficients

Linear Regression explains the relationship between each input feature and the target variable using regression coefficients.

A positive coefficient indicates that an increase in the feature tends to increase the predicted stock price, while a negative coefficient indicates the opposite.

The coefficient analysis showed that the current day's stock prices (**Open, High, Low, and Close**) had the strongest influence on predicting the next day's closing price.

## Feature Importance for Tree-Based Models

Decision Tree, Random Forest, and Gradient Boosting provide **feature importance scores** instead of regression coefficients.

These scores indicate how much each feature contributes to reducing prediction error during training.

![Image Description](f.png)


The feature importance analysis showed that:

- **Close** was the most influential feature.
- **High** and **Low** also contributed significantly.
- **Open** provided useful predictive information.
- **Volume** contributed less than the price-related features but still improved the model's predictions.

Overall, stock price features were more informative than trading volume for predicting the next day's closing price.

---

# 20. Visualizations Included

Several visualizations were created to better understand the dataset and evaluate the performance of the regression models.


---

## Visualization 1: Model Performance Comparison


<img src="./h.png" width="350">

This scatter plot compares the actual stock prices with the predicted prices from all models. Most points lie close to the diagonal line, showing that the predictions are very similar to the real values.

---

## Visualization 2: Residual Plot

![Image Description](g.png)


This graph shows the prediction errors made by each model. Most points are close to the zero line, meaning the models usually predicted values very close to the actual stock prices.

---

## Visualization 3: Prediction Error Distribution

![Stock Price Plot](i.png)

This graph shows how prediction errors are distributed for each model. Since most errors are centered around zero, it indicates that the models generally made small prediction mistakes and performed well.

---

# 21. Final Model Selection and Why

After training and evaluating all four regression models, **Linear Regression** was selected as the final model for this project.

## Reasons for Selecting Linear Regression

- Highest **R² (0.9536)** and lowest **MAE (1.2193)**, **RMSE (1.7181)**.
- Generalized well with **TimeSeriesSplit** validation.
- Simple, interpretable, and fast to train.
- Outperformed **Random Forest** and **Gradient Boosting** overall.

**Linear Regression** was selected for its best balance of **accuracy, simplicity, interpretability, and generalization**.

---

# 22. Conclusion

This project developed a machine learning model to predict the **next day's closing stock price** using historical **NYSE** data. After preprocessing, feature engineering, and chronological data splitting, four regression models were evaluated using **MAE, MSE, RMSE, R²**, and **TimeSeriesSplit** cross-validation. **Linear Regression** achieved the best performance (**R² = 0.9536**) with the lowest prediction errors, making it the most accurate model for this dataset. Overall, the project demonstrated a complete time-series regression workflow, from data preparation to model evaluation and selection.