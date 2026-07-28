# Customer Churn Prediction – Learning Report

## 1. Problem Statement

The objective of this project was to build a machine learning model that predicts whether a customer is likely to **churn (leave the company)** based on demographic information, subscribed services, contract type, billing details, and account history.

Customer churn prediction helps businesses identify customers who are at risk of leaving so they can take preventive actions such as offering discounts, improving services, or providing personalised retention plans.

---

## 2. How the Problem Was Solved

The project followed a complete machine learning workflow from raw data to model evaluation.

### Data Preparation

- Explored and understood the dataset.
- Identified the target variable (`Churn`).
- Handled missing values and corrected data types.
- Removed unnecessary columns (such as `customerID`).

### Data Preprocessing

- Split the dataset into training and testing sets.
- Applied **One-Hot Encoding** to categorical features.
- Applied **Standard Scaling** to numerical features.
- Used **ColumnTransformer** to preprocess different column types correctly.
- Combined preprocessing and modelling using a **Pipeline** to prevent data leakage.

### Model Training

The following machine learning algorithms were trained and compared:

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

### Model Evaluation

The models were evaluated using:

- Accuracy
- Confusion Matrix
- Precision
- Recall
- F1-Score
- ROC-AUC
- Cross Validation

The models were also analysed for:

- Overfitting and Underfitting
- Class Imbalance
- Feature Importance

---

## 3. Models Used, Why They Were Chosen

### Logistic Regression

#### Why was it chosen?

It is a simple and fast baseline classification algorithm. It performs well when the relationship between the features and the target is approximately linear.

#### What does it do?

It calculates the probability that a customer belongs to the **Churn** or **No Churn** class and predicts the class with the higher probability.

---

### Decision Tree

#### Why was it chosen?

Decision Trees are easy to interpret and can learn non-linear relationships without requiring feature scaling.

#### What does it do?

It repeatedly splits the data based on feature values until it reaches a decision about the customer's class.


---

### Random Forest

#### Why was it chosen?

Random Forest generally provides higher accuracy than a single Decision Tree by combining predictions from multiple trees.

#### What does it do?

It builds many Decision Trees using different random subsets of the data and combines their predictions through majority voting.


---

### Gradient Boosting

#### Why was it chosen?

Gradient Boosting is a powerful ensemble method that improves previous trees by focusing on correcting their mistakes.

#### What does it do?

It builds trees sequentially, where each new tree learns from the errors made by the previous trees.


---

## 4. Model Selection

After comparing all models using cross-validation and evaluation metrics, the best-performing model should be selected based on its ability to generalise to unseen data rather than only achieving high training accuracy.

The selection should consider:

- High validation performance.
- Balanced Precision and Recall.
- Low overfitting.
- Stable cross-validation scores.

---

# Key Learning Outcomes

During this project, I learned how to:

- Clean and prepare real-world datasets.
- Apply preprocessing techniques.
- Build reusable machine learning pipelines.
- Compare multiple classification algorithms.
- Perform cross-validation for reliable evaluation.
- Interpret confusion matrices and classification metrics.
- Detect overfitting and underfitting.
- Handle class imbalance using class weights and threshold tuning.
- Interpret feature importance while understanding its limitations.