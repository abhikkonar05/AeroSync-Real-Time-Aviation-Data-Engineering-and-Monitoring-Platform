CREATE DATABASE aerosync;

\c aerosync;

CREATE TABLE IF NOT EXISTS flights (
    flight_id VARCHAR PRIMARY KEY,
    airline VARCHAR,
    origin VARCHAR,
    destination VARCHAR,
    departure_time TIMESTAMP,
    arrival_time TIMESTAMP,
    delay_minutes INT,
    weather_condition VARCHAR
);

CREATE TABLE IF NOT EXISTS pipeline_logs (
    id SERIAL PRIMARY KEY,
    step VARCHAR,
    status VARCHAR,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);