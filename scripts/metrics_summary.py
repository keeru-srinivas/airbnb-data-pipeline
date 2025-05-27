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

print("\n Performing Groupby Aggregation by neighbourhood_group and room type.. \n")
group_agg = df.groupby(["neighbourhood group", "room type"])["total cost"].agg(["mean", "median", "count", "std"]).reset_index()
group_agg["coefficient_of_variation"] = group_agg["std"]/group_agg["mean"]

print("\n groupwise aggregation on output: \n")
print(group_agg)

group_agg.to_csv('data/cleaned/groupwise_price_stats.csv', index=False)

print("\n Saved groupwise stats to 'data/cleaned/groupwise_price_stats.csv'")

print("\n Performing price based feature engineering : \n")

#Log Transform-- so the expense or the long tails doesn't pull the data so the avg and the skew doesn't change 
df["log_total_cost"] = np.log1p(df["total cost"])

#price bucketing - to make the analysis easier when separated by bins 
bins = [0, 100, 250, 500, 1000, np.inf]
labels = ["very low", "low", "medium", "high", "luxury"]
df["price_bucket"] = pd.cut(df["total cost"], bins=bins, labels=labels)

#derived feature: price per minimum night 
if "minimum nights" in df.columns:
  df["price_per_min_stay"]= df["total cost"]/(df["minimum nights"].replace(0, np.nan))

#price rank with neighbourhood_group 
if "neighbourhood group" in df.columns:
  df["price_rank_within_area"]= df.groupby("neighbourhood group")["total cost"].rank(method = "dense", ascending=False)

print("\nSample of engineered features:\n")
print(df[['total cost', 'log_total_cost', 'price_bucket', 'price_per_min_stay', 'price_rank_within_area']].head())

df.to_csv("data/cleaned/airbnb_with_features.csv", index=False)
print("\n Saved enhanced dataset to 'data/cleaned/airbnb_with_features.csv'")



from sklearn.preprocessing import MinMaxScaler

print("\nPerforming normalization on selected features...\n")

# Select the columns you want to normalize
features_to_normalize = ['availability 365', 'reviews per month', 'price_per_min_stay', 'log_total_cost']

# Only keep the ones that actually exist (safety check)
features_to_normalize = [col for col in features_to_normalize if col in df.columns]

# Apply MinMaxScaler
scaler = MinMaxScaler()

# Scale and add new columns with "_scaled" suffix
for col in features_to_normalize:
    scaled_col = f"{col}_scaled"
    df[scaled_col] = scaler.fit_transform(df[[col]])
    print(f"Normalized '{col}' → '{scaled_col}'")

# Save updated dataset
df.to_csv("data/cleaned/airbnb_with_features.csv", index=False)
print("\nSaved final dataset with normalized features to 'data/cleaned/airbnb_with_features.csv'")



print("\nResetting and recreating: is_high_demand_listing...\n")

# Remove old version if it exists
if 'is_high_demand_listing' in df.columns:
    df.drop(columns=['is_high_demand_listing'], inplace=True)
    print(" Removed old 'is_high_demand_listing' column.")

# Create new column with default value
df['is_high_demand_listing'] = 0

# Softer logic: more listings should meet this threshold
high_demand_condition = (
    (df['reviews per month'] > 1.0) &
    (df['availability 365'] > 150) &
    (df['price_per_min_stay'] < 200)
)

# Apply the logic
df.loc[high_demand_condition, 'is_high_demand_listing'] = 1

# Show a quick result count
print("\n Demand flag summary:")
print(df['is_high_demand_listing'].value_counts())

# Save the final dataset
df.to_csv("data/cleaned/airbnb_with_features.csv", index=False)
print("\n Final dataset saved with updated 'is_high_demand_listing' column!")
