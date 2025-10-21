# Churn Prediction and Analysis – IBM Telco Dataset

## Overview
This project focuses on customer churn analysis and prediction modeling using the IBM Telco Customer Churn dataset.  
The goal is to identify key drivers behind customer churn and build an intelligent prediction system capable of forecasting whether a customer is likely to leave.

The repository includes:
- Comprehensive Exploratory Data Analysis (EDA) and statistical evaluation  
- Development and comparison of multiple Machine Learning models  
- A Streamlit web application that allows real-time churn prediction for future customers  

---

## Project Workflow

### 1. Data Analysis & Exploration
- Performed extensive EDA to understand customer demographics, services, and account information.  
- Used statistical and correlation analysis to determine top churn-driving features.  
- Visualized trends and distributions to highlight key retention factors.  

### 2. Feature Engineering
- Encoded categorical variables.  
- Handled missing values and outliers.  
- Engineered new features to improve model interpretability.  

### 3. Model Development
Compared several supervised learning algorithms:
- Logistic Regression  
- Random Forest  
- XGBoost (final model)  

XGBoost was selected for its superior performance and balance between precision and recall.  

### 4. Model Evaluation
- Evaluated models using accuracy, precision, recall, F1-score, ROC-AUC.  
- Conducted cross-validation for generalization assurance.  
- Produced interpretability plots to show top predictors of churn.  

### 5. Streamlit Application
A user-friendly Streamlit app was built to:
- Input customer attributes  
- Predict churn likelihood  
- Display model explanations interactively  

---

## Tech Stack
- Python  
- Pandas, NumPy  
- Matplotlib, Seaborn, Plotly  
- Scikit-learn, XGBoost  
- Streamlit  

---

