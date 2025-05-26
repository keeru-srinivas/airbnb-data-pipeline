import pandas as pd 
import numpy as np 

df = pd.read_csv("C:/Users/keert/OneDrive/Desktop/Data Engineering Projects/airbnb_project/data/raw/Airbnb_Open_Data.csv")

print(df.head())

print("The shape of the data is : ", df.shape)
print("\n columns: \n", df.columns.tolist())
print("\n  Missing values: \n", df.isnull().sum())
print("\n data types: \n", df.dtypes)

df["price"]=pd.to_numeric(df["price"].replace(r'[^\d.]', '', regex = True), errors="coerce")
df["service fee"] = pd.to_numeric(df["service fee"].replace(r'[^\d.]', '', regex = True), errors = "coerce")

print(df[["price", "service fee"]].dtypes)

df["last review"] = pd.to_datetime(df["last review"], errors = 'coerce')
print(df["last review"].dtypes)

df["reviews per month"] = df["reviews per month"].fillna(0)
df["house_rules"] = df["house_rules"].fillna(0)

df = df.drop(columns= ["license"])

df["total cost"]= df["price"] + df["service fee"]


print("\n  Missing values: \n", df.isnull().sum())

string_cols = ["NAME", "host name", "country", "country code", "cancellation_policy", "instant_bookable", "neighbourhood", "neighbourhood group","host_identity_verified"]
for col in string_cols:
  df[col]=df[col].fillna("Not Provided")

  print("\n  Missing values: \n", df.isnull().sum())

df["minimum nights"] = df["minimum nights"].fillna(df["minimum nights"].median())
df["Construction year"] =df["Construction year"].fillna(0)
df["service fee"] = df["service fee"].fillna(0)
df["last review"] = df["last review"].fillna(0)
df["review rate number"] = df["review rate number"].fillna(0)
df["calculated host listings count"] = df["calculated host listings count"].fillna(0)
df["availability 365"] = df["availability 365"].fillna(0)
df["total cost"] = df["total cost"].fillna(0)
df["number of reviews"] = df["number of reviews"].fillna(0)

print("\n missing values: \n", df.isnull().sum())

df = df.dropna(subset = ["lat", "long"])

df = df.dropna(subset = ["price"])

print("\n missing values: \n", df.isnull().sum())
print(df.shape)

print("\n data types: \n", df.dtypes)
df.to_csv("C:/Users/keert/OneDrive/Desktop/Data Engineering Projects/airbnb_project/data/cleaned/airbnb_cleaned.csv", index=False)

print(df.head())