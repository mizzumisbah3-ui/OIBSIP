import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

iris = load_iris()

df = pd.DataFrame(iris.data, columns=iris.feature_names)

df["Species"] = iris.target

species_names = {
    0: "Setosa",
    1: "Versicolor",
    2: "Virginica"
}

df["Species"] = df["Species"].map(species_names)

print("First 5 Rows")
print(df.head())

print("\nShape of Dataset")
print(df.shape)

print("\nData Types")
print(df.dtypes)

print("\nMissing Values")
print(df.isnull().sum())

print("\nStatistical Summary")
print(df.describe())

print("\nClass Distribution")
print(df["Species"].value_counts())

sns.pairplot(df, hue="Species")
plt.show()

plt.figure(figsize=(10,6))
sns.boxplot(data=df.iloc[:,0:4])
plt.title("Feature Distribution")
plt.show()

print("\nFeature Selection")
print("Petal Length and Petal Width are the most useful features for identifying flower species.")

X = df.drop("Species", axis=1)
y = df["Species"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

log_model = LogisticRegression(max_iter=200)

log_model.fit(X_train, y_train)

log_prediction = log_model.predict(X_test)

print("\nLogistic Regression Results")

log_accuracy = accuracy_score(y_test, log_prediction)

print("Accuracy :", log_accuracy)

print("\nConfusion Matrix")
print(confusion_matrix(y_test, log_prediction))

print("\nClassification Report")
print(classification_report(y_test, log_prediction))

tree_model = DecisionTreeClassifier(random_state=42)

tree_model.fit(X_train, y_train)

tree_prediction = tree_model.predict(X_test)

print("\nDecision Tree Results")

tree_accuracy = accuracy_score(y_test, tree_prediction)

print("Accuracy :", tree_accuracy)

print("\nConfusion Matrix")
print(confusion_matrix(y_test, tree_prediction))

print("\nClassification Report")
print(classification_report(y_test, tree_prediction))

print("\nModel Comparison")

print("Logistic Regression Accuracy :", round(log_accuracy,4))
print("Decision Tree Accuracy       :", round(tree_accuracy,4))

if log_accuracy > tree_accuracy:
    print("\nBest Model : Logistic Regression")
elif tree_accuracy > log_accuracy:
    print("\nBest Model : Decision Tree")
else:
    print("\nBoth models performed equally well.")
