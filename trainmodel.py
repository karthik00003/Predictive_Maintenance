import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# -------------------------
# 1. LOAD DATASET
# -------------------------
data = pd.read_csv("vehicletypee.csv")   # make sure this is your NEW dataset


# -------------------------
# 2. ENCODE CATEGORICAL DATA
# -------------------------
vehicle_map = {"Hatchback":0, "Sedan":1, "SUV":2, "Truck":3}
tire_map = {"Good":0, "Moderate":1, "Worn":2, "Critical":3}
vibration_map = {"Low":0, "Medium":1, "High":2}
accident_map = {"No":0, "Yes":1}

data["Vehicle_Type"] = data["Vehicle_Type"].map(vehicle_map)
data["Tire_Condition"] = data["Tire_Condition"].map(tire_map)
data["Vibration_Level"] = data["Vibration_Level"].map(vibration_map)
data["Accident_History"] = data["Accident_History"].map(accident_map)


# -------------------------
# 3. USE EXACT TARGET (NO CONVERSION)
# -------------------------
y = data["Remaining_KM"]


# -------------------------
# 4. DEFINE FEATURES
# -------------------------
X = data[[
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
]]


# -------------------------
# 5. TRAIN-TEST SPLIT
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# -------------------------
# 6. MODEL (IMPROVED)
# -------------------------
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=9,
    min_samples_split=35,
    min_samples_leaf=15,
    random_state=42
)


# -------------------------
# 7. TRAIN
# -------------------------
model.fit(X_train, y_train)


# -------------------------
# 8. PREDICT
# -------------------------
y_pred = model.predict(X_test)


# -------------------------
# 9. REGRESSION METRICS
# -------------------------
# 9. RANGE FUNCTION (for evaluation only)
# -------------------------
def get_range(km):
    if km <= 3000:
        return "0–3000"
    elif km <= 10000:
        return "3001–10000"
    elif km <= 25000:
        return "10001–25000"
    elif km <= 50000:
        return "25001–50000"
    elif km <= 80000:
        return "50001–80000"
    else:
        return "80001+"


# Convert both actual & predicted into ranges
y_test_range = [get_range(v) for v in y_test]
y_pred_range = [get_range(v) for v in y_pred]


# -------------------------
# 10. METRICS
# -------------------------
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

accuracy = accuracy_score(y_test_range, y_pred_range)
precision = precision_score(y_test_range, y_pred_range, average='weighted', zero_division=0)
recall = recall_score(y_test_range, y_pred_range, average='weighted', zero_division=0)
f1 = f1_score(y_test_range, y_pred_range, average='weighted', zero_division=0)

mae = mean_absolute_error(y_test, y_pred)


print("\n--- MODEL PERFORMANCE ---")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"MAE       : {mae:.2f}")


# -------------------------
# 11. SAVE MODEL
# -------------------------
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(X.columns, open("columns.pkl", "wb"))
print("\nModel saved successfully!")