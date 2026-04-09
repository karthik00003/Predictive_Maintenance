# Vehi Care - Vehicle Maintenance Predictor

An AI-powered vehicle health monitoring platform that predicts remaining useful life based on idle-state sensor data.

## Features

- **AI-Powered Predictions**: Uses a trained Random Forest model to predict vehicle remaining useful life in kilometers
- **Multi-Vehicle Support**: Optimized for Hatchback, Sedan, SUV, and Truck classifications
- **Real-Time Analysis**: Fast predictions based on engine vitals, electrical health, and tire conditions
- **User Authentication**: Simple login/signup system
- **Analytics Dashboard**: View fleet health statistics and trends
- **Modern UI**: Responsive design with glassmorphism effects

## Requirements

- Python 3.7+
- Virtual Environment (recommended)

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd /Users/karthik/Desktop/predictive
   ```

2. **Create/activate virtual environment** (if not already created):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Using the run script (Recommended)
```bash
./run.sh
```

### Option 2: Manual activation
```bash
source .venv/bin/activate
python3 app.py
```

The application will start on `http://127.0.0.1:5000`

## Using the Application

1. **Login**: Navigate to the login page and enter any username and password to proceed
2. **Home Page**: View information about the application and get started
3. **Prediction Dashboard**: 
   - Enter vehicle specifications (type, age, mileage)
   - Provide engine vitals (RPM, temperature, oil pressure, fuel consumption)
   - Fill electrical and safety metrics (battery voltage, brake/tire pressure)
   - Submit to get remaining useful life prediction
4. **Analysis**: View fleet statistics and trends
5. **About**: Learn more about Vehi Care

## Data Features

The model uses 14 key features:

### General Specs
- Vehicle Type (Hatchback, Sedan, SUV, Truck)
- Vehicle Age (0-15 years)
- Total Mileage (km)
- Last Service Duration (months)

### Engine Vitals (at Idle)
- RPM (700-1000 range)
- Engine Temperature (°C)
- Oil Pressure (PSI)
- Fuel Consumption (km/l)

### Electrical & Safety
- Battery Voltage (V)
- Brake Pressure (PSI)
- Tire Pressure (PSI)
- Accident History (Yes/No)

### Sensory Analysis
- Tire Condition (Good/Moderate/Worn/Critical)
- Vibration Level (Low/Medium/High)

## Model Training

To retrain the model with updated data:

```bash
source .venv/bin/activate
python3 trainmodel.py
```

The script will:
1. Load the vehicle dataset from `vehicletypee.csv`
2. Train a Random Forest Regressor
3. Display performance metrics (Accuracy, Precision, Recall, F1 Score, MAE)
4. Save the trained model as `model.pkl`

## Database

User data is stored in SQLite:
- `users.db`: User login information (optional - fully functional without it)

To reset the database:
```bash
source .venv/bin/activate
python3 database.py
```

## API Endpoints

- `GET /` - Login page
- `POST /login` - Handle login (any username/password accepted for demo)
- `POST /signup` - Handle signup (redirects to home)
- `GET /home` - Home/Dashboard page (requires login)
- `GET /predict_page` - Prediction page (requires login)
- `POST /predict` - Get AI prediction (returns JSON)
- `GET /logout` - Logout and redirect to login

## File Structure

```
predictive/
├── app.py              # Flask application main file
├── trainmodel.py       # Model training script
├── database.py         # Database initialization
├── requirements.txt    # Python dependencies
├── run.sh             # Run script
├── model.pkl          # Trained ML model
├── columns.pkl        # Feature column names
├── users.db           # SQLite database
├── templates/
│   ├── login.html     # Login page
│   ├── index.html     # Main dashboard (home, predict, analysis, about)
│   ├── form.html      # Prediction form (reference)
│   └── result.html    # Result template (reference)
└── static/            # CSS and JavaScript assets
    ├── style.css
    ├── index.js
    └── login.css
```

## Model Performance

The trained Random Forest model achieves:
- **Accuracy**: ~85-90% on range predictions
- **Mean Absolute Error**: ±3,000-5,000 km
- **Training**: Uses 80/20 train-test split

## Troubleshooting

### Module not found errors
- Ensure virtual environment is activated: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

### Port already in use
- Flask runs on port 5000 by default
- Kill existing process: `pkill -f "python3 app.py"`
- Or modify port in `app.py`: Change `app.run()` to `app.run(port=5001)`

### Model file missing
- Retrain the model: `python3 trainmodel.py`
- Ensure `vehicletypee.csv` exists in the project directory

## Development Notes

- **Debug Mode**: Enabled by default (`app.run(debug=True)`)
- **Secret Key**: Change `app.secret_key` in production
- **CORS**: Not configured - add Flask-CORS if needed for APIs
- **Static Files**: CSS/JS served from `static/` directory via Flask

## Future Enhancements

- [ ] Real OBD-II integration for actual vehicle data
- [ ] User prediction history and export
- [ ] Mobile app for on-the-go predictions
- [ ] Multi-language support
- [ ] Actual user authentication with password hashing
- [ ] Cloud deployment (AWS/Heroku)

## License

This project is open source and available for educational purposes.

---

**Vehi Care Team** - Making predictive vehicle maintenance intelligent and accessible.
