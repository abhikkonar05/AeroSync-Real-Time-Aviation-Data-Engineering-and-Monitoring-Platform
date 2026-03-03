
import pandas as pd
import os

def transform_data():

    # Make sure processed folder exists
    os.makedirs("data_lake/processed", exist_ok=True)

    # 1️⃣ Read both datasets
    flights = pd.read_csv("data_lake/raw/flights/flights.csv")
    weather = pd.read_csv("data_lake/raw/weather/weather.csv")

    print("Flights Columns:", flights.columns)
    print("Weather Columns:", weather.columns)

    # 2️⃣ Merge them
    merged = pd.merge(
        flights,
        weather,
        left_on="origin",     # column in flights
        right_on="airport",   # column in weather
        how="left"            # keep all flights
    )

    # 3️⃣ Drop duplicate column
    merged.drop(columns=["airport"], inplace=True)

    # 4️⃣ Save to processed folder
    merged.to_csv("data_lake/processed/cleaned_data.csv", index=False)

    print("Merge successful ✅")

    return merged