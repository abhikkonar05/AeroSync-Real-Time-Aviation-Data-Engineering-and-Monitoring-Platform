from etl.extract_flights import extract_flight_data
from etl.extract_weather import extract_weather_data
from etl.transform import transform_data
from etl.load import load_to_db
from data_quality.checks import validate_data
from data_quality.validation_report import print_validation_report
from monitoring.logger import log_step

def run_pipeline():
    try:
        log_step("Extraction", "Started")
        extract_flight_data()
        extract_weather_data()
        log_step("Extraction", "Completed")

        log_step("Transformation", "Started")
        df = transform_data()
        log_step("Transformation", "Completed")

        log_step("Validation", "Started")
        errors = validate_data(df)
        print_validation_report(errors)

        if not errors:
            log_step("Loading", "Started")
            load_to_db()
            log_step("Loading", "Completed")
            print("Pipeline executed successfully 🎉")
        else:
            log_step("Loading", "Failed")

    except Exception as e:
        print("Pipeline failed:", e)

if __name__ == "__main__":
    run_pipeline()