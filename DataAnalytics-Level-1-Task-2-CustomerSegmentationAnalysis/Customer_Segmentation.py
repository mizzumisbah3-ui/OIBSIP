import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv("ecommerce_customer_data.csv")


print("Dataset Loaded Successfully\n")

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


for column in df.select_dtypes(include=np.number):
    df[column].fillna(
        df[column].median(),
        inplace=True
    )


print("\nAfter Cleaning:")
print(df.isnull().sum())


print("\nStatistical Summary:")
print(df.describe())


print("\nAvailable Columns:")
print(df.columns)


features = df[
    [
        "Time on App",
        "Time on Website",
        "Length of Membership",
        "Yearly Amount Spent"
    ]
]


print("\nSelected Features:")
print(features.head())


scaler = StandardScaler()

scaled_features = scaler.fit_transform(features)


scaled_features = pd.DataFrame(
    scaled_features,
    columns=features.columns
)


print("\nScaled Data:")
print(scaled_features.head())


wcss = []


for i in range(1, 11):

    kmeans = KMeans(
        n_clusters=i,
        random_state=42,
        n_init=10
    )

    kmeans.fit(scaled_features)

    wcss.append(kmeans.inertia_)


plt.figure(figsize=(8,5))

plt.plot(
    range(1,11),
    wcss,
    marker="o"
)

plt.title("Elbow Method")

plt.xlabel("Number of Clusters")

plt.ylabel("WCSS")

plt.grid()

plt.show()


kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)


df["Cluster"] = kmeans.fit_predict(
    scaled_features
)


print("\nCluster Distribution:")
print(df["Cluster"].value_counts())


plt.figure(figsize=(8,6))


sns.scatterplot(
    data=df,
    x="Length of Membership",
    y="Yearly Amount Spent",
    hue="Cluster",
    s=100
)


plt.title("Customer Segmentation")

plt.xlabel("Annual Income")

plt.ylabel("Spending Score")

plt.show()


cluster_profile = (
    df.groupby("Cluster")
    [
        [
            "Time on App",
            "Time on Website",
            "Length of Membership",
            "Yearly Amount Spent"
        ]
    ]
    .mean()
)


print("\nCluster Profile:")

print(cluster_profile)


plt.figure(figsize=(7,4))


sns.countplot(
    data=df,
    x="Cluster"
)


plt.title("Customers per Cluster")

plt.show()


plt.figure(figsize=(8,5))


sns.boxplot(
    data=df,
    x="Cluster",
    y="Yearly Amount Spent"
)

plt.title("Spending Behaviour by Cluster")

plt.show()


print("""
CUSTOMER SEGMENTATION INSIGHTS:

Cluster 0:
Average spending customers suitable for regular promotions.

Cluster 1:
High income and high spending customers suitable for premium products and loyalty programs.

Cluster 2:
Low spending customers who can be targeted with discounts.

Cluster 3:
Potential customers who need personalized marketing strategies.

RECOMMENDATIONS:

1. Provide loyalty rewards for high-value customers.

2. Create personalized offers based on customer segments.

3. Improve engagement with low-spending customers.

4. Use customer groups for targeted marketing campaigns.
""")


df.to_csv(
    "customer_segments.csv",
    index=False
)


print("\nCustomer segmentation file saved successfully!")
