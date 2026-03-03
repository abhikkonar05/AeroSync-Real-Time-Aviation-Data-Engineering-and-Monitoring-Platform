import pandas as pd
import random
import os

def extract_weather_data():
    os.makedirs("data_lake/raw/weather", exist_ok=True)

    data = []
    for airport in ["DEL", "BLR", "CCU"]:
        data.append({
            "airport": airport,
            "weather_condition": random.choice(["Clear", "Rain", "Fog"])
        })

    df = pd.DataFrame(data)
    df.to_csv("data_lake/raw/weather/weather.csv", index=False)
    return df