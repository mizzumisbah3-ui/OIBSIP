import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

df = pd.read_csv("Unemployment in India.csv")

print("First 5 Rows")
print(df.head())

print("\nShape of Dataset")
print(df.shape)

print("\nDataset Information")
print(df.info())

df.columns = df.columns.str.strip()

df.rename(columns={
    "Estimated Unemployment Rate (%)": "Unemployment Rate",
    "Estimated Employed": "Employed",
    "Estimated Labour Participation Rate (%)": "Labour Participation Rate"
}, inplace=True)

print("\nMissing Values")
print(df.isnull().sum())

df.dropna(inplace=True)

df["Date"] = pd.to_datetime(df["Date"])

print("\nData Types")
print(df.dtypes)

print("\nStatistical Summary")
print(df.describe())

region_avg = df.groupby("Region")["Unemployment Rate"].mean().sort_values(ascending=False)

plt.figure(figsize=(14,6))
sns.barplot(
    x=region_avg.index,
    y=region_avg.values,
    hue=region_avg.index,
    palette="viridis",
    legend=False
)
plt.title("Average Unemployment Rate by Region")
plt.xlabel("Region")
plt.ylabel("Average Unemployment Rate (%)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

df["Month"] = df["Date"].dt.month_name()

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly_avg = df.groupby("Month")["Unemployment Rate"].mean().reindex(month_order)

plt.figure(figsize=(12,6))
sns.lineplot(
    x=monthly_avg.index,
    y=monthly_avg.values,
    marker="o",
    linewidth=2
)
plt.title("Average Monthly Unemployment Rate")
plt.xlabel("Month")
plt.ylabel("Average Unemployment Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

states = ["Maharashtra", "Tamil Nadu", "Karnataka"]

state_df = df[df["Region"].isin(states)]

plt.figure(figsize=(14,6))
sns.lineplot(
    data=state_df,
    x="Date",
    y="Unemployment Rate",
    hue="Region",
    marker="o"
)
plt.title("Unemployment Rate Over Time")
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.legend(title="State")
plt.tight_layout()
plt.show()

top10 = (
    df.groupby("Region")["Unemployment Rate"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6))
sns.barplot(
    x=top10.values,
    y=top10.index,
    hue=top10.index,
    palette="rocket",
    legend=False
)
plt.title("Top 10 States with Highest Average Unemployment Rate")
plt.xlabel("Average Unemployment Rate (%)")
plt.ylabel("State")
plt.tight_layout()
plt.show()

corr = df[[
    "Unemployment Rate",
    "Employed",
    "Labour Participation Rate"
]].corr()

plt.figure(figsize=(8,6))
sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

covid_date = pd.Timestamp("2020-03-25")

pre_covid = df[df["Date"] < covid_date]
post_covid = df[df["Date"] >= covid_date]

print("\nAverage Unemployment Rate Before COVID")
print(pre_covid["Unemployment Rate"].mean())

print("\nAverage Unemployment Rate After COVID")
print(post_covid["Unemployment Rate"].mean())

comparison = pd.DataFrame({
    "Period": ["Pre-COVID", "Post-COVID"],
    "Average Unemployment Rate": [
        pre_covid["Unemployment Rate"].mean(),
        post_covid["Unemployment Rate"].mean()
    ]
})

plt.figure(figsize=(6,5))
sns.barplot(
    data=comparison,
    x="Period",
    y="Average Unemployment Rate",
    hue="Period",
    palette=["green", "red"],
    legend=False
)
plt.title("Pre-COVID vs Post-COVID Unemployment Rate")
plt.ylabel("Average Unemployment Rate (%)")
plt.tight_layout()
plt.show()

print("\nAnalysis Completed Successfully!")
