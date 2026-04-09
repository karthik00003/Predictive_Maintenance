import pandas as pd
import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# -------------------------
# 1. LOAD DATASET
# -------------------------
data = pd.read_csv("final_vehicle_dataset.csv")
print(f"Dataset loaded: {data.shape}")
print(f"Columns: {list(data.columns)}")


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

print("Categorical encoding done")


# -------------------------
# 3. CONVERT KM_RANGE TO NUMERIC VALUES
# -------------------------
def range_to_value(km_range):
    """Convert KM range strings to midpoint values"""
    km_str = str(km_range).strip()
    
    if '0' in km_str and '3' in km_str and '000' in km_str:
        return 1500
    elif '3' in km_str and '10' in km_str and '000' in km_str:
        return 6500
    elif '10' in km_str and '25' in km_str and '000' in km_str:
        return 17500
    elif '25' in km_str and '50' in km_str and '000' in km_str:
        return 37500
    elif '50' in km_str and '80' in km_str and '000' in km_str:
        return 65000
    elif '80' in km_str and '+' in km_str:
        return 100000
    else:
        return 50000

y = data["KM_Range_Before_Defect"].apply(range_to_value)
print(f"Target values created: min={y.min()}, max={y.max()}, mean={y.mean():.0f}")


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

print(f"Features shape: {X.shape}")


# -------------------------
# 5. TRAIN-TEST SPLIT
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")


# -------------------------
# 6. MODEL (OPTIMIZED)
# -------------------------
model = RandomForestRegressor(
    n_estimators=150,
    max_depth=12,
    min_samples_split=20,
    min_samples_leaf=10,
    random_state=42,
    n_jobs=-1
)

print("Training model...")
model.fit(X_train, y_train)
print("Model training complete!")


# -------------------------
# 7. PREDICTIONS
# -------------------------
y_pred = model.predict(X_test)


# -------------------------
# 8. EVALUATION METRICS
# -------------------------
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\n" + "="*50)
print("MODEL PERFORMANCE METRICS")
print("="*50)
print(f"Mean Absolute Error (MAE):   {mae:,.2f} km")
print(f"Root Mean Squared Error (RMSE): {rmse:,.2f} km")
print(f"R² Score:                    {r2:.4f}")
print("="*50)

# Feature importance
feature_importance = sorted(
    zip(X.columns, model.feature_importances_),
    key=lambda x: x[1],
    reverse=True
)
print("\nTop 5 Most Important Features:")
for i, (feature, importance) in enumerate(feature_importance[:5], 1):
    print(f"  {i}. {feature}: {importance:.4f}")


# -------------------------
# 9. SAVE MODEL
# -------------------------
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(X.columns, open("columns.pkl", "wb"))
print("\n✓ Model saved to model.pkl")
print("✓ Columns saved to columns.pkl")
