# Daily Progress Report

## Topics Learned
- Machine Learning fundamentals
- Supervised vs Unsupervised Learning
- Classification vs Regression
- Features (X) and Target (y)
- Training and Prediction
- Train, Validation, and Test Split
- Generalisation
- Overfitting and Underfitting
- K-Fold Cross Validation
- Stratified K-Fold Cross Validation
- Logistic Regression (Introduction)
- Machine Learning workflow
- Data encoding for machine learning

---

## Tasks Completed
- Understood the complete Machine Learning workflow from data to model evaluation.
- Identified the Telco Customer Churn problem as a **Binary Classification** task.
- Identified **Churn** as the target variable and selected the remaining columns as features.
- Learned the difference between supervised and unsupervised learning.
- Understood the purpose of training, validation, and test datasets.
- Learned why datasets are split before training a model.
- Understood the concepts of generalisation, overfitting, and underfitting.
- Studied K-Fold and Stratified K-Fold Cross Validation.
- Loaded the cleaned Telco Customer Churn dataset into Jupyter Notebook.
- Separated the dataset into feature matrix (**X**) and target vector (**y**).
- Performed an 80/20 train-test split using `train_test_split()`.
- Created a baseline Logistic Regression model.
- Identified that machine learning models require numerical input features.
- Applied appropriate encoding techniques:
  - Label Encoding
  - Ordinal Encoding
  - One-Hot Encoding
- Performed 5-Fold Stratified Cross Validation.
- Calculated and interpreted:
  - Cross-validation accuracy
  - Mean accuracy
  - Standard deviation

---

## Key Findings
- The Telco Customer Churn dataset is a **Supervised Learning** dataset.
- The prediction problem is a **Binary Classification** problem.
- Machine learning models cannot train directly on string (categorical) values.
- All categorical features must be encoded into numerical values before model training.
- Train/Test Split helps evaluate model performance on unseen data.
- Cross Validation provides a more reliable estimate of model performance than a single train-test split.
- Stratified K-Fold preserves the class distribution in each fold, making it suitable for classification tasks.
- Mean Accuracy measures the average model performance across all folds.
- Standard Deviation measures the consistency of model performance.

---

## Problems Faced
- Logistic Regression failed to train during cross-validation.
- Received the error:
  ```
  ValueError: could not convert string to float: 'Male'
  ```
- The dataset still contained categorical columns with string values.
- Cross-validation could not proceed because the model requires numerical input features.

---

## Solution
- Inspected feature data types using `df.dtypes`.
- Identified all categorical columns stored as string (`str`) data types.
- Applied:
  - Label Encoding for binary categorical features.
  - Ordinal Encoding for the `Contract` column.
  - One-Hot Encoding for nominal categorical features.
- Recreated the train-test split using the encoded dataset.
- Successfully executed Stratified 5-Fold Cross Validation.

---

## Next Day Plan
- Dummy Baseline
- Logistic Regression
- Trees, Random Forest & Gradient Boosting
- Encoding, Scaling & Pipelines
