import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve
)

from imblearn.over_sampling import SMOTE

import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv("creditcard.csv")


print("Dataset Loaded Successfully")

print(df.head())


print("\nDataset Shape:")
print(df.shape)


print("\nDataset Information:")
print(df.info())


print("\nMissing Values:")
print(df.isnull().sum())


print("\nDuplicate Values:")
print(df.duplicated().sum())


df.drop_duplicates(inplace=True)


print("\nDataset Shape After Removing Duplicates:")
print(df.shape)



print("\nClass Distribution:")
print(df["Class"].value_counts())


fraud_count = df["Class"].value_counts()[1]

total_count = len(df)


print("\nFraud Percentage:")

print(
    (fraud_count / total_count) * 100
)



plt.figure(figsize=(6,4))

sns.countplot(
    data=df,
    x="Class"
)

plt.title(
    "Fraud vs Non-Fraud Transactions"
)

plt.show()



plt.figure(figsize=(8,5))

sns.histplot(
    data=df,
    x="Amount",
    hue="Class",
    bins=50
)

plt.title(
    "Transaction Amount Distribution"
)

plt.show()



plt.figure(figsize=(10,5))

sns.histplot(
    data=df,
    x="Time",
    hue="Class",
    bins=100
)

plt.title(
    "Transaction Time Analysis"
)

plt.show()



plt.figure(figsize=(14,10))

sns.heatmap(
    df.corr(),
    cmap="coolwarm",
    center=0
)

plt.title(
    "Correlation Heatmap"
)

plt.show()

X = df.drop(
    "Class",
    axis=1
)

y = df["Class"]



X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)



scaler = StandardScaler()


X_train["Amount"] = scaler.fit_transform(
    X_train[["Amount"]]
)


X_test["Amount"] = scaler.transform(
    X_test[["Amount"]]
)



smote = SMOTE(
    random_state=42
)


X_train_balanced, y_train_balanced = smote.fit_resample(
    X_train,
    y_train
)



print("\nAfter SMOTE:")

print(
    y_train_balanced.value_counts()
)



logistic_model = LogisticRegression(
    max_iter=500,
    n_jobs=-1
)



random_forest_model = RandomForestClassifier(
    n_estimators=50,
    random_state=42,
    n_jobs=-1
)

print("Training Logistic Regression...")

logistic_model.fit(
    X_train_balanced,
    y_train_balanced
)

print("Training Random Forest...")

random_forest_model.fit(
    X_train_balanced,
    y_train_balanced
)



models = {

    "Logistic Regression": logistic_model,

    "Random Forest": random_forest_model

}



for name, model in models.items():


    prediction = model.predict(
        X_test
    )


    probability = model.predict_proba(
        X_test
    )[:,1]



    print("\n==============================")

    print(
        "Model:",
        name
    )

    print("==============================")



    print(
        classification_report(
            y_test,
            prediction
        )
    )



    print(
        "Precision:",
        precision_score(
            y_test,
            prediction
        )
    )


    print(
        "Recall:",
        recall_score(
            y_test,
            prediction
        )
    )


    print(
        "F1 Score:",
        f1_score(
            y_test,
            prediction
        )
    )


    print(
        "ROC-AUC:",
        roc_auc_score(
            y_test,
            probability
        )
    )



    cm = confusion_matrix(
        y_test,
        prediction
    )



    plt.figure(figsize=(5,4))


    sns.heatmap(
        cm,
        annot=True,
        fmt="d"
    )



    plt.title(
        name + " Confusion Matrix"
    )


    plt.xlabel(
        "Predicted"
    )


    plt.ylabel(
        "Actual"
    )


    plt.show()

    rf_probability = random_forest_model.predict_proba(
    X_test
)[:,1]



fpr, tpr, thresholds = roc_curve(
    y_test,
    rf_probability
)



plt.figure(figsize=(7,5))


plt.plot(
    fpr,
    tpr
)


plt.title(
    "ROC Curve - Random Forest"
)


plt.xlabel(
    "False Positive Rate"
)


plt.ylabel(
    "True Positive Rate"
)


plt.show()



importance = pd.DataFrame(
    {
        "Feature": X.columns,
        "Importance": random_forest_model.feature_importances_
    }
)



importance = importance.sort_values(
    by="Importance",
    ascending=False
)



plt.figure(figsize=(10,6))


sns.barplot(
    data=importance.head(10),
    x="Importance",
    y="Feature"
)


plt.title(
    "Top Feature Importance"
)


plt.show()



importance.to_csv(
    "feature_importance.csv",
    index=False
)



results = X_test.copy()


results["Actual"] = y_test.values


results["Predicted"] = random_forest_model.predict(
    X_test
)



results.to_csv(
    "Fraud_Predictions.csv",
    index=False
)



print("""
FRAUD DETECTION INSIGHTS:

1. The dataset is highly imbalanced, where fraudulent transactions are very small compared to normal transactions.

2. Accuracy is not a reliable metric for fraud detection because the majority class can dominate the results.

3. Recall is an important metric because missing a fraudulent transaction can cause financial loss.

4. SMOTE improves model performance by balancing fraud and non-fraud transaction samples.

5. Random Forest performs well because it can learn complex patterns from transaction features.


SCALABILITY DISCUSSION:

For handling millions of transactions:

- Deploy the trained model using a real-time API.
- Use streaming platforms like Kafka for transaction processing.
- Use distributed processing tools like Spark for large datasets.
- Retrain the model periodically with new fraud patterns.
- Monitor model performance continuously.
""")



print(
    "\nFraud Detection Analysis Completed Successfully!"
)
