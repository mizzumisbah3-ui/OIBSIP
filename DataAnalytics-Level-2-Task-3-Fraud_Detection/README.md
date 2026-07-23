# Fraud Detection

## Project Overview

This project is completed as part of the **Data Analytics Level 2 (Task 3)**.

The objective of this project is to build a machine learning pipeline to identify fraudulent financial transactions from a highly imbalanced credit card transaction dataset.

The project focuses on handling class imbalance, applying machine learning algorithms, and evaluating model performance using appropriate fraud detection metrics.

## Task Details

**Track:** Data Analytics  
**Level:** Level 2  
**Task Number:** Task 3  
**Task Name:** Fraud Detection  

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Imbalanced-learn (SMOTE)
- Matplotlib
- Seaborn

## Dataset

Dataset Used:

Credit Card Fraud Detection Dataset

Dataset Information:

- Total Transactions: 284,807
- Fraudulent Transactions: 492
- Legitimate Transactions: 284,315

The dataset contains anonymized transaction features and a Class column:
- 0 → Normal Transaction
- 1 → Fraudulent Transaction

## Project Features

✔ Loaded and explored transaction dataset  
✔ Performed data quality checks  
✔ Analyzed class imbalance  
✔ Calculated fraud percentage  
✔ Visualized fraud distribution  
✔ Analyzed transaction amount patterns  
✔ Applied SMOTE for balancing classes  
✔ Built Logistic Regression model  
✔ Built Random Forest classification model  
✔ Evaluated models using Precision, Recall, F1-score, and ROC-AUC  
✔ Generated confusion matrices  
✔ Created ROC curve visualization  
✔ Analyzed feature importance  

## Machine Learning Models

### 1. Logistic Regression

Used as a baseline classification model for fraud prediction.

### 2. Random Forest Classifier

Used to capture complex relationships between transaction features and improve prediction performance.

## Evaluation Metrics

The models were evaluated using:

- Precision
- Recall
- F1 Score
- ROC-AUC Score
- Confusion Matrix

Recall is especially important in fraud detection because identifying fraudulent transactions is more critical than overall accuracy.

## Key Insights

- Fraud transactions represent a very small percentage of total transactions.
- SMOTE improves model learning by balancing fraud and legitimate classes.
- Random Forest can identify complex transaction patterns effectively.
- Feature importance helps understand which transaction attributes influence predictions.

## Business Recommendations

- Implement real-time fraud monitoring systems.
- Use machine learning models to flag suspicious transactions.
- Continuously retrain models with new fraud patterns.
- Combine automated detection with manual verification for high-risk transactions.


## Conclusion

This project demonstrates practical experience in handling imbalanced datasets, applying machine learning algorithms, evaluating fraud detection models, and extracting actionable insights from financial transaction data.
