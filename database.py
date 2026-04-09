import sqlite3
from datetime import datetime

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Vehicles table
cursor.execute("""
CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    vehicle_type TEXT NOT NULL,
    make TEXT,
    model TEXT,
    year INTEGER,
    vin TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

# Prediction history table
cursor.execute("""
CREATE TABLE IF NOT EXISTS prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    vehicle_type TEXT,
    vehicle_age REAL,
    mileage REAL,
    engine_temp REAL,
    rpm REAL,
    oil_pressure REAL,
    fuel_consumption REAL,
    battery_voltage REAL,
    brake_pressure REAL,
    tire_pressure REAL,
    tire_condition TEXT,
    vibration_level TEXT,
    last_service_months REAL,
    accident_history TEXT,
    prediction_result INTEGER,
    prediction_range TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
)
""")

# Anomaly detection table
cursor.execute("""
CREATE TABLE IF NOT EXISTS anomalies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    sensor_name TEXT NOT NULL,
    measured_value REAL,
    normal_range_min REAL,
    normal_range_max REAL,
    alert_level TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved INTEGER DEFAULT 0,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
)
""")

conn.commit()
conn.close()

print("Database schema updated successfully!")