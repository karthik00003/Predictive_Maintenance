from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import pandas as pd

app = Flask(__name__)
app.secret_key = "secret123"


# -------------------------
# LOAD MODEL
# -------------------------
reg = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))


# -------------------------
# ENCODING MAPS (same as training)
# -------------------------
vehicle_map = {"Hatchback":0, "Sedan":1, "SUV":2, "Truck":3}
tire_map = {"Good":0, "Moderate":1, "Worn":2, "Critical":3}
vibration_map = {"Low":0, "Medium":1, "High":2}
accident_map = {"No":0, "Yes":1}

# -------------------------
# SAFE FLOAT
# -------------------------
def safe_float(x):
    return float(x) if x and x.strip() != "" else 0.0


# -------------------------
# GET RANGE FUNCTION
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
# LOGIN PAGE
# -------------------------
@app.route('/')
def login():
    return render_template("login.html")


# -------------------------
# LOGIN CHECK
# -------------------------
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "karthik" and password == "1234":
        session["user"] = username
        return redirect(url_for('home'))
    else:
        return render_template("login.html", error="Invalid credentials")


# -------------------------
# HOME PAGE
# -------------------------
@app.route('/home')
def home():
    if "user" not in session:
        return redirect(url_for('login'))
    return render_template("index.html")


# -------------------------
# FORM PAGE
# -------------------------
@app.route('/predict_page')
def predict_page():
    if "user" not in session:
        return redirect(url_for('login'))
    return render_template("form.html")


# -------------------------
# PREDICTION
# -------------------------
@app.route('/predict', methods=['POST'])
def predict():

    if "user" not in session:
        return redirect(url_for('login'))

    try:
        data = {
            "Vehicle_Type": vehicle_map[request.form.get("Vehicle_Type")],
            "Vehicle_Age": safe_float(request.form.get("Vehicle_Age")),
            "Mileage": safe_float(request.form.get("Mileage")),
            "Engine_Temp": safe_float(request.form.get("Engine_Temp")),
            "RPM": safe_float(request.form.get("RPM")),
            "Oil_Pressure": safe_float(request.form.get("Oil_Pressure")),
            "Fuel_Consumption": safe_float(request.form.get("Fuel_Consumption")),
            "Battery_Voltage": safe_float(request.form.get("Battery_Voltage")),
            "Brake_Pressure": safe_float(request.form.get("Brake_Pressure")),
            "Tire_Pressure": safe_float(request.form.get("Tire_Pressure")),
            "Tire_Condition": tire_map[request.form.get("Tire_Condition")],
            "Vibration_Level": vibration_map[request.form.get("Vibration_Level")],
            "Last_Service_Months": safe_float(request.form.get("Last_Service_Months")),
            "Accident_History": accident_map[request.form.get("Accident_History")]
        }

        # Convert to dataframe
        df = pd.DataFrame([data])

        # Ensure same column order
        df = df.reindex(columns=columns, fill_value=0)

        # Predict
        exact_pred = int(reg.predict(df)[0])
        range_pred = get_range(exact_pred)

        return render_template(
            "result.html",
            range_pred=range_pred,
            exact_pred=exact_pred
        )

    except Exception as e:
        return f"Error: {e}"


# -------------------------
# LOGOUT
# -------------------------
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)