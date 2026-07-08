# Car Price Prediction with Machine Learning

## Overview

This project was completed as part of the **Oasis Infobyte Data Science Internship** under the **Data Science Track (Task 3).**

The objective of this project was to build a machine learning regression model capable of predicting the selling price of used cars based on various features such as car age, present price, kilometers driven, fuel type, seller type, transmission, ownership, and brand.

The project involved data cleaning, feature engineering, exploratory data analysis (EDA), model training, evaluation, and comparison to identify the best-performing regression model.

---

## Features

- Loaded the CarDekho vehicle dataset
- Performed data cleaning by checking missing values and removing duplicate records
- Standardized categorical values for consistency
- Created a new **Car Age** feature from the manufacturing year
- Extracted the **Brand** from the car name
- Performed Exploratory Data Analysis (EDA)
- Visualized selling price distribution using a histogram
- Compared selling price by fuel type using a box plot
- Analyzed selling price against car age using a scatter plot
- Generated a feature correlation heatmap
- Encoded categorical variables using One-Hot Encoding
- Split the dataset into training and testing sets
- Trained two regression models:
  - Linear Regression
  - Random Forest Regressor
- Evaluated both models using:
  - Mean Absolute Error (MAE)
  - Root Mean Squared Error (RMSE)
  - R² Score
- Compared model performance and selected the best-performing model
- Visualized feature importance for the best model

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Visual Studio Code
---

## Project Workflow

1. Imported the required Python libraries.
2. Loaded the CarDekho dataset.
3. Cleaned the dataset by checking missing values and removing duplicates.
4. Performed feature engineering by creating Car Age and Brand features.
5. Conducted Exploratory Data Analysis (EDA).
6. Encoded categorical variables.
7. Split the dataset into training and testing sets.
8. Trained Linear Regression and Random Forest Regression models.
9. Evaluated model performance using MAE, RMSE, and R² Score.
10. Compared the models and selected the best-performing regression model.
11. Visualized feature importance.

---

## Learning Outcomes

Through this project, I gained practical experience in:

- Data cleaning and preprocessing
- Feature engineering
- Exploratory Data Analysis (EDA)
- Data visualization
- Encoding categorical variables
- Regression modeling
- Model evaluation and comparison
- Understanding feature importance in machine learning

---

## Results

Both Linear Regression and Random Forest Regressor were trained and evaluated on the dataset.

After comparing the evaluation metrics (MAE, RMSE, and R² Score), **Linear Regression** achieved the best overall performance and was selected as the final model for predicting used car selling prices.

---

## Author

**Anjum Misbah Z**
---

