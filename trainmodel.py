import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# -------------------------
# 1. LOAD DATASET
# -------------------------
data = pd.read_csv("datasetnew.csv")


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
# 3. GET RANGE FUNCTION
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
        return "80001–120000"


# -------------------------
# 4. RANGE → NUMERIC (for regression)
# -------------------------
def convert_km_range(value):

    if isinstance(value, str):
        value = value.strip().strip('"').replace(',', '')

        if value.endswith('+'):
            value = value[:-1]
            return float(value) * 1.2

        if '–' in value or '-' in value:
            parts = value.replace('–', '-').split('-')
            if len(parts) == 2:
                start = float(parts[0].strip())
                end = float(parts[1].strip())
                return (start + end) / 2

        return float(value)

    return float(value)


# Create numeric target
data["Remaining_KM"] = data["KM_Range_Before_Defect"].apply(convert_km_range)


# -------------------------
# 4. FEATURES
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

# Targets
y_class = data["Remaining_KM"].apply(get_range)
y_reg   = data["Remaining_KM"]


# -------------------------
# 5. TRAIN-TEST SPLIT
# -------------------------
X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
    X, y_class, y_reg, test_size=0.2, random_state=42
)


# -------------------------
# 6. MODELS
# -------------------------
clf = DecisionTreeClassifier(
    max_depth=12,
    min_samples_split=20,
    min_samples_leaf=10,
    random_state=42
)

reg = DecisionTreeRegressor(
    max_depth=12,
    min_samples_split=20,
    min_samples_leaf=10,
    random_state=42
)


# -------------------------
# 7. TRAIN
# -------------------------
clf.fit(X_train, y_class_train)
reg.fit(X_train, y_reg_train)


# -------------------------
# 8. PREDICT
# -------------------------
y_class_pred = clf.predict(X_test)
y_reg_pred   = reg.predict(X_test)

# -------------------------
# 9. EVALUATION
# -------------------------


# --- Classification Metrics ---
accuracy = accuracy_score(y_class_test, y_class_pred)
precision = precision_score(y_class_test, y_class_pred, average='weighted', zero_division=0)
recall = recall_score(y_class_test, y_class_pred, average='weighted', zero_division=0)
f1 = f1_score(y_class_test, y_class_pred, average='weighted', zero_division=0)

# --- Regression Metric ---
mae = mean_absolute_error(y_reg_test, y_reg_pred)

# --- Print Results ---
print("\n--- MODEL PERFORMANCE ---")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"MAE       : {mae:.2f}")


# -------------------------
# 10. SAVE MODELS
# -------------------------
pickle.dump(clf, open("classifier.pkl", "wb"))
pickle.dump(reg, open("regressor.pkl", "wb"))
pickle.dump(X.columns, open("columns.pkl", "wb"))

print("\nBoth models saved successfully!")
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# -------------------------
# 1. LOAD DATASET
# -------------------------
data = pd.read_csv("datasetnew.csv")


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
# 3. GET RANGE FUNCTION
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
        return "80001–120000"


# -------------------------
# 4. RANGE → NUMERIC (for regression)
# -------------------------
def convert_km_range(value):

    if isinstance(value, str):
        value = value.strip().strip('"').replace(',', '')

        if value.endswith('+'):
            value = value[:-1]
            return float(value) * 1.2

        if '–' in value or '-' in value:
            parts = value.replace('–', '-').split('-')
            if len(parts) == 2:
                start = float(parts[0].strip())
                end = float(parts[1].strip())
                return (start + end) / 2

        return float(value)

    return float(value)


# Create numeric target
data["Remaining_KM"] = data["KM_Range_Before_Defect"].apply(convert_km_range)


# -------------------------
# 4. FEATURES
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

# Targets
y_class = data["Remaining_KM"].apply(get_range)
y_reg   = data["Remaining_KM"]


# -------------------------
# 5. TRAIN-TEST SPLIT
# -------------------------
X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
    X, y_class, y_reg, test_size=0.2, random_state=42
)


# -------------------------
# 6. MODELS
# -------------------------
clf = DecisionTreeClassifier(
    max_depth=12,
    min_samples_split=20,
    min_samples_leaf=10,
    random_state=42
)

reg = DecisionTreeRegressor(
    max_depth=12,
    min_samples_split=20,
    min_samples_leaf=10,
    random_state=42
)


# -------------------------
# 7. TRAIN
# -------------------------
clf.fit(X_train, y_class_train)
reg.fit(X_train, y_reg_train)


# -------------------------
# 8. PREDICT
# -------------------------
y_class_pred = clf.predict(X_test)
y_reg_pred   = reg.predict(X_test)

# -------------------------
# 9. EVALUATION
# -------------------------

# -------------------------
# 9. EVALUATION (ONLY REGRESSOR)
# -------------------------

# Convert regression predictions → range
y_reg_pred_range = [get_range(val) for val in y_reg_pred]

# Actual ranges
y_actual_range = [get_range(val) for val in y_reg_test]

# --- Classification Metrics (based on regressor output) ---
accuracy = accuracy_score(y_actual_range, y_reg_pred_range)
precision = precision_score(y_actual_range, y_reg_pred_range, average='weighted', zero_division=0)
recall = recall_score(y_actual_range, y_reg_pred_range, average='weighted', zero_division=0)
f1 = f1_score(y_actual_range, y_reg_pred_range, average='weighted', zero_division=0)

# --- Regression Metric ---
mae = mean_absolute_error(y_reg_test, y_reg_pred)

# --- Print Results ---
print("\n--- REGRESSOR PERFORMANCE ---")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"MAE       : {mae:.2f}")

# -------------------------
# 10. SAVE MODELS
# -------------------------
pickle.dump(clf, open("classifier.pkl", "wb"))
pickle.dump(reg, open("regressor.pkl", "wb"))
pickle.dump(X.columns, open("columns.pkl", "wb"))

print("\nBoth models saved successfully!")


