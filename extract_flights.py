import pandas as pd
import random
from datetime import datetime
import os

def extract_flight_data():
    os.makedirs("data_lake/raw/flights", exist_ok=True)

    data = []
    for i in range(10):
        data.append({
            "flight_id": f"FL{i}",
            "airline": random.choice(["IndiGo", "Air India", "SpiceJet"]),
            "origin": random.choice(["DEL", "BLR", "CCU"]),
            "destination": random.choice(["BOM", "HYD", "MAA"]),
            "departure_time": datetime.now(),
            "arrival_time": datetime.now(),
            "delay_minutes": random.randint(0, 120)
        })

    df = pd.DataFrame(data)
    df.to_csv("data_lake/raw/flights/flights.csv", index=False)
    return df