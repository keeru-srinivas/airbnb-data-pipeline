import pandas as pd
raw = pd.read_csv("data/raw/Airbnb_Open_Data.csv")
cleaned = pd.read_csv("data/cleaned/airbnb_cleaned.csv")

if 'availability_365' in raw.columns and 'availability 365' not in cleaned.columns:
    merged = cleaned.merge(
        raw[['id', 'availability_365']],
        on='id',
        how='left'
    )

    merged.rename(columns={'availability_365': 'availability 365'}, inplace=True)

    merged.to_csv("data/cleaned/airbnb_cleaned.csv", index=False)
    print(" Successfully added 'availability 365' to cleaned dataset!")
else:
    print(" Column already present or missing in raw data.")


