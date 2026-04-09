# QUICK START GUIDE - VEHI CARE

## 🚀 5-Minute Setup

### Step 1: Navigate to Project
```bash
cd /Users/karthik/Desktop/predictive
```

### Step 2: Run the Application
```bash
./run.sh
```

That's it! The app will start at **http://127.0.0.1:5000**

---

## 🔐 Using the App

### Login
- Use **any username and password** (demo mode)
- Click "Login" to proceed

### Make a Prediction
1. Click "Predict" in the navigation bar
2. Fill in vehicle details:
   - **Vehicle Type**: Select Hatchback, Sedan, SUV, or Truck
   - **Age**: Years since manufacture
   - **Mileage**: Total kilometers traveled
   - **Service**: Months since last service
3. Enter engine vitals at idle:
   - RPM, Engine Temperature, Oil Pressure
   - Fuel Consumption rate
4. Provide electrical & safety metrics:
   - Battery Voltage, Brake Pressure, Tire Pressure
   - Accident history
5. Assess tire condition and vibration
6. Click "Calculate Remaining KM"

### View Results
- **Predicted Range**: Estimated kilometers remaining (with ±range)
- **Color Badge**: 
  - 🟢 Green = Good Health (>40,000 km)
  - 🟡 Yellow = Service Soon (15,000-40,000 km)
  - 🔴 Red = Critical (< 15,000 km)

---

## 📊 Features

- **Analytics**: View fleet statistics and trends
- **About**: Learn more about the app
- **Logout**: End your session

---

## ⚙️ Troubleshooting

### App won't start?
```bash
# Activate venv manually
source .venv/bin/activate
python3 app.py
```

### Port 5000 already in use?
```bash
# Kill the process
pkill -f "python3 app.py"

# Then run again
./run.sh
```

### Need to retrain model?
```bash
source .venv/bin/activate
python3 trainmodel.py
```

---

## 📁 Project Structure
```
predictive/
├── app.py              ← Main Flask app
├── trainmodel.py       ← Model training
├── test_app.py         ← Tests (run: python3 test_app.py)
├── run.sh              ← Start script
├── requirements.txt    ← Dependencies
├── model.pkl          ← ML model
├── columns.pkl        ← Feature names
└── templates/
    ├── login.html
    ├── index.html (home/predict/analysis)
    ├── form.html (reference)
    └── result.html (reference)
```

---

## ✅ Status
- **Code**: ✓ Fixed & Optimized
- **Tests**: ✓ All Passing
- **Ready**: ✓ Yes, Ready to Run

Start with: `./run.sh`

---

**Vehi Care** - Predictive Vehicle Maintenance Made Easy
