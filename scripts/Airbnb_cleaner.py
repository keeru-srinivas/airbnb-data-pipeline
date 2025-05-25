import pandas as pd 
import numpy as np 

df = pd.read_csv("Airbnb_listings_nyc/Airbnb_Open_Data.csv")

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

df.to_csv("Airbnb_listings_nyc/airbnb_cleaned.csv", index=False)
print(" Cleaned data saved successfully to another file called airbnb_cleaned.csv")

print(df)
