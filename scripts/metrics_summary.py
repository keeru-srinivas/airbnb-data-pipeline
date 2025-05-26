import pandas as pd
import numpy as np

df = pd.read_csv("C:/Users/keert/OneDrive/Desktop/Data Engineering Projects/airbnb_project/data/cleaned/airbnb_cleaned.csv")

numeric_cols= df.select_dtypes(include = [np.number])
print("numberic columns in the dataset:")
print(numeric_cols)

summary_df =pd.DataFrame({
  "Columns":numeric_cols.columns,
  "Min": numeric_cols.min().values,
  "Max": numeric_cols.max().values,
  "Mean": numeric_cols.mean().values,
  "Std Dev": numeric_cols.std().values,
  "Skewness": numeric_cols.skew().values,
  "Kurtosis": numeric_cols.kurt().values

})

print("\n  summary statistics: \n")
print(summary_df)

summary_df.to_csv("data/cleaned/numeric_summary.csv", index=False)
print("\n Saved summary to 'data/cleaned/numeric_summary.csv'")