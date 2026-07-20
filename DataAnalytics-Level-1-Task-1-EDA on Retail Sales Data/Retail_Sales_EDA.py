import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("Online Retail.csv")

print("Dataset Loaded Successfully\n")

print("First 5 Rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)


print("\nDataset Information:")
print(df.info())


print("\nMissing Values:")
print(df.isnull().sum())


print("\nDuplicate Rows:")
print(df.duplicated().sum())

df.drop_duplicates(inplace=True)

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])


print("\nAfter Cleaning:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe())


print("\nMean:")
print(df.mean(numeric_only=True))


print("\nMedian:")
print(df.median(numeric_only=True))


print("\nMode:")
print(df.mode().iloc[0])


print("\nStandard Deviation:")
print(df.std(numeric_only=True))

if "Date" in df.columns:

    df["Month"] = df["Date"].dt.to_period("M")

    monthly_sales = df.groupby("Month")["Total Amount"].sum()

    plt.figure(figsize=(12,5))

    monthly_sales.plot(
        marker="o"
    )

    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")

    plt.xticks(rotation=45)

    plt.grid()
    plt.show()

if "Date" in df.columns:

    df["Quarter"] = df["Date"].dt.to_period("Q")

    quarterly_sales = df.groupby("Quarter")["Total Amount"].sum()

    plt.figure(figsize=(8,5))

    quarterly_sales.plot(
        marker="o"
    )

    plt.title("Quarterly Sales Trend")
    plt.xlabel("Quarter")
    plt.ylabel("Sales")

    plt.grid()

    plt.show()

if "Age" in df.columns:

    plt.figure(figsize=(8,5))

    sns.histplot(
        df["Age"],
        bins=10,
        kde=True
    )

    plt.title("Customer Age Distribution")

    plt.show()


if "Gender" in df.columns:

    plt.figure(figsize=(6,4))

    sns.countplot(
        data=df,
        x="Gender"
    )

    plt.title("Customer Gender Distribution")

    plt.show()


if "Product Category" in df.columns:

    top_products = (
        df.groupby("Product Category")["Quantity"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )


    print("\nTop Selling Products:")
    print(top_products)


    plt.figure(figsize=(10,5))


    sns.barplot(
        x=top_products.values,
        y=top_products.index
    )


    plt.title(
        "Top 10 Best Selling Products"
    )

    plt.xlabel(
        "Quantity Sold"
    )

    plt.show()


if "Product Category" in df.columns:

    category_sales = (
        df.groupby("Product Category")
        ["Total Amount"]
        .sum()
        .sort_values(
            ascending=False
        )
    )


    print("\nRevenue By Category:")
    print(category_sales)


    plt.figure(figsize=(10,5))


    sns.barplot(
        x=category_sales.values,
        y=category_sales.index
    )


    plt.title(
        "Revenue By Product Category"
    )

    plt.xlabel(
        "Revenue"
    )

    plt.show()


numeric_data = df.select_dtypes(
    include=np.number
)


plt.figure(figsize=(8,6))


sns.heatmap(
    numeric_data.corr(),
    annot=True,
    cmap="coolwarm"
)


plt.title(
    "Correlation Matrix"
)


plt.show()


if "Age" in df.columns:

    df["Age Group"] = pd.cut(
        df["Age"],
        bins=[
            0,
            20,
            40,
            60,
            100
        ],
        labels=[
            "Teen",
            "Adult",
            "Middle Age",
            "Senior"
        ]
    )


    plt.figure(figsize=(8,5))


    sns.countplot(
        data=df,
        x="Age Group"
    )


    plt.title(
        "Customers By Age Group"
    )


    plt.show()


print("""
BUSINESS RECOMMENDATIONS:

1. Identify high-sales months and run promotional campaigns during those periods.

2. Maintain higher inventory for best-selling product categories.

3. Use customer demographic information to create personalized marketing strategies.

4. Analyze customer age groups to improve product targeting.

5. Focus on categories generating maximum revenue for business growth.
""")


df.to_csv(
    "cleaned_retail_sales_dataset.csv",
    index=False
)


print("\nCleaned dataset saved successfully!")
