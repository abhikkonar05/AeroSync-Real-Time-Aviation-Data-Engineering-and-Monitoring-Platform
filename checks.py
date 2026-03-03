def validate_data(df):
    errors = []

    if df["flight_id"].isnull().sum() > 0:
        errors.append("Missing flight IDs")

    if (df["delay_minutes"] < 0).any():
        errors.append("Negative delay found")

    return errors