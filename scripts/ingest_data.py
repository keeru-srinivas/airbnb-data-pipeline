import pandas as pd

# Load the raw Airbnb dataset
df = pd.read_csv("data/raw/Airbnb_Open_Data.csv")

# Preview the shape
print("📦 Raw dataset loaded. Shape:", df.shape)
