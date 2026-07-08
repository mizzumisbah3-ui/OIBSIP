import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

df = pd.read_csv("car data.csv")

print("First 5 Rows")
print(df.head())

print("\nShape of Dataset")
print(df.shape)

print("\nData Types")
print(df.dtypes)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

df = df.drop_duplicates()

df["Fuel_Type"] = df["Fuel_Type"].str.title()
df["Seller_Type"] = df["Seller_Type"].str.title()
df["Transmission"] = df["Transmission"].str.title()

current_year = 2025
df["Car_Age"] = current_year - df["Year"]

df["Brand"] = df["Car_Name"].apply(lambda x: x.split()[0])

print("\nUpdated Dataset")
print(df.head())

plt.figure(figsize=(8,5))
sns.histplot(df["Selling_Price"], bins=20, kde=True)
plt.title("Distribution of Selling Price")
plt.xlabel("Selling Price")
plt.ylabel("Count")
plt.show()

plt.figure(figsize=(7,5))
sns.boxplot(x="Fuel_Type", y="Selling_Price", data=df)
plt.title("Selling Price vs Fuel Type")
plt.show()

plt.figure(figsize=(7,5))
sns.scatterplot(x="Car_Age", y="Selling_Price", data=df)
plt.title("Selling Price vs Car Age")
plt.show()

numeric_df = df.select_dtypes(include=["number"])

plt.figure(figsize=(10,7))
sns.heatmap(numeric_df.corr(), annot=True, cmap="Blues")
plt.title("Correlation Heatmap")
plt.show()

X = df.drop(["Selling_Price", "Car_Name", "Year"], axis=1)
y = df["Selling_Price"]

categorical_columns = ["Fuel_Type", "Seller_Type", "Transmission", "Brand"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_columns)
    ],
    remainder="passthrough"
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

linear_model = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LinearRegression())
])

linear_model.fit(X_train, y_train)

linear_prediction = linear_model.predict(X_test)

linear_mae = mean_absolute_error(y_test, linear_prediction)
linear_rmse = np.sqrt(mean_squared_error(y_test, linear_prediction))
linear_r2 = r2_score(y_test, linear_prediction)

print("\nLinear Regression Results")
print("MAE :", round(linear_mae,2))
print("RMSE :", round(linear_rmse,2))
print("R2 Score :", round(linear_r2,2))

forest_model = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ))
])

forest_model.fit(X_train, y_train)

forest_prediction = forest_model.predict(X_test)

forest_mae = mean_absolute_error(y_test, forest_prediction)
forest_rmse = np.sqrt(mean_squared_error(y_test, forest_prediction))
forest_r2 = r2_score(y_test, forest_prediction)

print("\nRandom Forest Results")
print("MAE :", round(forest_mae,2))
print("RMSE :", round(forest_rmse,2))
print("R2 Score :", round(forest_r2,2))

print("\nModel Comparison")
print("Linear Regression R2 :", round(linear_r2,2))
print("Random Forest R2 :", round(forest_r2,2))

if forest_r2 > linear_r2:
    print("\nBest Model : Random Forest Regressor")
else:
    print("\nBest Model : Linear Regression")

encoded_columns = forest_model.named_steps["preprocessor"].get_feature_names_out()

importance = forest_model.named_steps["model"].feature_importances_

importance_df = pd.DataFrame({
    "Feature": encoded_columns,
    "Importance": importance
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

plt.figure(figsize=(10,6))
sns.barplot(
    data=importance_df.head(10),
    x="Importance",
    y="Feature"
)
plt.title("Top 10 Feature Importance")
plt.show()
