import pandas as pd
from database.connection import engine
from sqlalchemy import text

def load_to_db():
    df = pd.read_csv("data_lake/processed/cleaned_data.csv")

    # Avoid inserting duplicate flights by checking existing flight_ids
    with engine.connect() as conn:
        try:
            existing = conn.execute(text("SELECT flight_id FROM flights")).fetchall()
            existing_ids = {r[0] for r in existing}
        except Exception:
            existing_ids = set()

    new_df = df[~df['flight_id'].isin(existing_ids)]
    if new_df.empty:
        print("No new flights to insert")
        return

    new_df.to_sql("flights", engine, if_exists="append", index=False)