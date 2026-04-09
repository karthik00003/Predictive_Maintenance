# =========================================
# SHARED MODEL CONFIGURATION & UTILITIES
# =========================================

# Encoding maps for categorical features
vehicle_map = {"Hatchback": 0, "Sedan": 1, "SUV": 2, "Truck": 3}
tire_map = {"Good": 0, "Moderate": 1, "Worn": 2, "Critical": 3}
vibration_map = {"Low": 0, "Medium": 1, "High": 2}
accident_map = {"No": 0, "Yes": 1}

# Reverse maps for display
vehicle_reverse = {v: k for k, v in vehicle_map.items()}
tire_reverse = {v: k for k, v in tire_map.items()}
vibration_reverse = {v: k for k, v in vibration_map.items()}
accident_reverse = {v: k for k, v in accident_map.items()}

# Feature list used in model training
FEATURE_LIST = [
    "Vehicle_Type",
    "Vehicle_Age",
    "Mileage",
    "Engine_Temp",
    "RPM",
    "Oil_Pressure",
    "Fuel_Consumption",
    "Battery_Voltage",
    "Brake_Pressure",
    "Tire_Pressure",
    "Tire_Condition",
    "Vibration_Level",
    "Last_Service_Months",
    "Accident_History"
]

# Prediction range categorization
def get_range(km):
    """
    Convert exact KM prediction to categorical range.
    Used in trainmodel.py for evaluation and in app.py for display.
    """
    if km <= 1000:
        return "0–1000"
    elif km <= 3000:
        return "1001–3000"
    elif km <= 7000:
        return "3001–7000"
    elif km <= 15000:
        return "7001–15000"
    elif km <= 25000:
        return "15001–25000"
    elif km <= 45000:
        return "30001–45000"
    elif km <= 60000:
        return "45000–60000"
    elif km <= 80000:
        return "60000–80000"
    else:
        return "80000+"
