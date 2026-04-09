from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
import pickle
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import io
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch
from model_utils import (
    vehicle_map, tire_map, vibration_map, accident_map,
    vehicle_reverse, tire_reverse, vibration_reverse, accident_reverse,
    get_range, FEATURE_LIST
)

app = Flask(__name__)
app.secret_key = "secret123"

# Database helper
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))
try:
    feature_names = pickle.load(open("columns.pkl", "rb"))
except:
    feature_names = None

# Reverse maps for display (imported from model_utils above)
# Anomaly detection function
def detect_anomalies(data):
    anomalies = []
    
    # Normal ranges based on vehicle diagnostics
    ranges = {
        "RPM": (700, 1000),
        "Engine_Temp": (80, 105),
        "Oil_Pressure": (25, 45),
        "Fuel_Consumption": (5, 20),
        "Battery_Voltage": (12, 14.5),
        "Brake_Pressure": (30, 45),
        "Tire_Pressure": (30, 35),
        "Vehicle_Age": (0, 15),
        "Mileage": (0, 350000),
    }
    
    for param, (min_val, max_val) in ranges.items():
        if param in data:
            value = float(data.get(param, 0))
            if value < min_val:
                anomalies.append({
                    "sensor": param,
                    "value": value,
                    "min": min_val,
                    "max": max_val,
                    "level": "WARNING",
                    "message": f"{param} is below normal range"
                })
            elif value > max_val:
                anomalies.append({
                    "sensor": param,
                    "value": value,
                    "min": min_val,
                    "max": max_val,
                    "level": "WARNING",
                    "message": f"{param} is above normal range"
                })
    
    return anomalies


# Health status function based on remaining KM range
def get_health_status(km):
    """
    Determine vehicle health status based on remaining KM prediction.
    """
    if km <= 1000:
        return "CRITICAL - Immediate Maintenance Required"
    elif km <= 3000:
        return "SEVERE - Urgent Maintenance Needed"
    elif km <= 7000:
        return "POOR - Maintenance Required Soon"
    elif km <= 15000:
        return "FAIR - Schedule Maintenance"
    elif km <= 25000:
        return "GOOD - Routine Maintenance Recommended"
    elif km <= 45000:
        return "VERY GOOD - Maintain Regular Service"
    elif km <= 60000:
        return "EXCELLENT - Vehicle in Excellent Condition"
    elif km <= 80000:
        return "EXCEPTIONAL - Outstanding Vehicle Health"
    else:
        return "VEHICLE IN GOOD HEALTH"


# ---------------- RANGE & HEALTH STATUS (NO get_range) ----------------
def get_range_and_status(km):
    if km <= 1000:
        return ("0–1000", "CRITICAL - Immediate Maintenance Required")
    elif km <= 3000:
        return ("1001–3000", "SEVERE - Urgent Maintenance Needed")
    elif km <= 7000:
        return ("3001–7000", "POOR - Maintenance Required Soon")
    elif km <= 15000:
        return ("7001–15000", "FAIR - Schedule Maintenance")
    elif km <= 25000:
        return ("15001–25000", "GOOD - Routine Maintenance Recommended")
    elif km <= 45000:
        return ("30001–45000", "VERY GOOD - Maintain Regular Service")
    elif km <= 60000:
        return ("45000–60000", "EXCELLENT - Vehicle in Excellent Condition")
    elif km <= 80000:
        return ("60000–80000", "EXCEPTIONAL - Outstanding Vehicle Health")
    else:
        return ("80000+", "VEHICLE IN GOOD HEALTH")


# ---------------- LOGIN PAGE ----------------
@app.route('/')
def login_page():
    return render_template('login.html')


# ---------------- HANDLE LOGIN ----------------
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    print("DEBUG LOGIN:", username, password)  # 👈 helps debugging

    # Validate against database
    if username and password:
        try:
            db = sqlite3.connect('users.db')
            cursor = db.cursor()
            cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            db.close()
            
            if user and user[1] == password:  # Check if user exists and password matches
                session["user"] = username
                session["user_id"] = user[0]  # Store user_id for database queries
                # Handle AJAX requests with JSON response
                if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({"success": True, "redirect": url_for('home')})
                return redirect(url_for('home'))
            else:
                # Invalid credentials
                if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({"success": False, "error": "Invalid credentials"}), 401
                return render_template('login.html', error="Invalid credentials")
        except Exception as e:
            print(f"Login error: {e}")
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": False, "error": "Login error"}), 500
            return render_template('login.html', error="Login error")
    else:
        # Handle AJAX requests with JSON response
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"success": False, "error": "Invalid credentials"}), 401
        # Render login page with error message for non-AJAX requests
        return render_template('login.html', error="Invalid credentials")


# --------- HOME PAGE ---------
@app.route('/home')
def home():
    if "user" not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html')

@app.route('/predict_page')
def predict_page():
    if "user" not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('login_page'))

# --------- MULTI-VEHICLE MANAGEMENT ---------
@app.route('/vehicles', methods=['GET', 'POST', 'DELETE'])
def vehicles():
    if "user" not in session or "user_id" not in session:
        return redirect(url_for('login_page'))
    
    user_id = session["user_id"]
    
    if request.method == 'POST':
        data = request.json
        db = get_db()
        try:
            db.execute("""
                INSERT INTO vehicles (user_id, vehicle_type, make, model, year, vin)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, data.get('type'), data.get('make'), data.get('model'),
                  data.get('year'), data.get('vin')))
            db.commit()
            return jsonify({"success": True, "message": "Vehicle added"})
        except Exception as e:
            return jsonify({"error": str(e)})
        finally:
            db.close()
    
    # GET request - get vehicles for current user only
    db = get_db()
    vehicles_list = db.execute("SELECT * FROM vehicles WHERE user_id = ?", (user_id,)).fetchall()
    db.close()
    
    vehicles_data = []
    for v in vehicles_list:
        vehicles_data.append({
            "id": v['id'],
            "type": v['vehicle_type'],
            "make": v['make'],
            "model": v['model'],
            "year": v['year'],
            "vin": v['vin'],
            "health_status": "Unknown"  # Will be calculated based on latest prediction
        })
    
    return jsonify({"vehicles": vehicles_data})

@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    if "user" not in session or "user_id" not in session:
        return redirect(url_for('login_page'))
    
    user_id = session["user_id"]
    db = get_db()
    try:
        # Check that this vehicle belongs to the current user
        vehicle = db.execute("SELECT user_id FROM vehicles WHERE id = ?", (vehicle_id,)).fetchone()
        if not vehicle or vehicle['user_id'] != user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        db.execute("DELETE FROM vehicles WHERE id = ?", (vehicle_id,))
        db.commit()
        return jsonify({"success": True, "message": "Vehicle deleted"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db.close()

@app.route('/vehicle/<int:vehicle_id>/history')
def vehicle_history(vehicle_id):
    if "user" not in session or "user_id" not in session:
        return redirect(url_for('login_page'))
    
    user_id = session["user_id"]
    db = get_db()
    
    # Check that this vehicle belongs to the current user
    vehicle = db.execute("SELECT user_id FROM vehicles WHERE id = ?", (vehicle_id,)).fetchone()
    if not vehicle or vehicle['user_id'] != user_id:
        db.close()
        return jsonify({"error": "Unauthorized"}), 403
    
    history = db.execute("""
        SELECT * FROM prediction_history WHERE vehicle_id = ?
        ORDER BY created_at DESC LIMIT 50
    """, (vehicle_id,)).fetchall()
    db.close()
    
    history_data = []
    for h in history:
        history_data.append({
            "vehicle_id": h['vehicle_id'],
            "timestamp": h['created_at'],
            "predicted_km": h['prediction_result'],
            "prediction_range": h['prediction_range'],
            "mileage": h['mileage'],
            "engine_temp": h['engine_temp'],
            "rpm": h['rpm']
        })
    
    return jsonify({"history": history_data})

@app.route('/vehicle/<int:vehicle_id>/anomalies')
def vehicle_anomalies(vehicle_id):
    if "user" not in session or "user_id" not in session:
        return redirect(url_for('login_page'))
    
    user_id = session["user_id"]
    db = get_db()
    
    # Check that this vehicle belongs to the current user
    vehicle = db.execute("SELECT user_id FROM vehicles WHERE id = ?", (vehicle_id,)).fetchone()
    if not vehicle or vehicle['user_id'] != user_id:
        db.close()
        return jsonify({"error": "Unauthorized"}), 403
    
    anomalies = db.execute("""
        SELECT * FROM anomalies WHERE vehicle_id = ?
        ORDER BY created_at DESC
    """, (vehicle_id,)).fetchall()
    db.close()
    
    anomalies_data = []
    for a in anomalies:
        anomalies_data.append({
            "id": a['id'],
            "vehicle_id": a['vehicle_id'],
            "parameter": a['sensor_name'],
            "actual_value": a['measured_value'],
            "normal_range": f"{a['normal_range_min']} - {a['normal_range_max']}",
            "severity": a['alert_level'].lower(),
            "status": "resolved" if a.get('resolved') == 1 else "unresolved",
            "timestamp": a['created_at'],
            "description": a['description']
        })
    
    return jsonify({"anomalies": anomalies_data})

@app.route('/vehicle/<int:vehicle_id>/export-pdf')
def export_pdf(vehicle_id):
    if "user" not in session:
        return redirect(url_for('login_page'))
    
    db = get_db()
    vehicle = db.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,)).fetchone()
    history = db.execute("""
        SELECT * FROM prediction_history WHERE vehicle_id = ?
        ORDER BY created_at DESC LIMIT 10
    """, (vehicle_id,)).fetchall()
    anomalies = db.execute("""
        SELECT * FROM anomalies WHERE vehicle_id = ?
        ORDER BY created_at DESC LIMIT 5
    """, (vehicle_id,)).fetchall()
    db.close()
    
    # Create PDF
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#00c6ff'),
        spaceAfter=30,
        alignment=1
    )
    elements.append(Paragraph("Vehicle Health Prediction Report", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Vehicle info - Make it prominent
    if vehicle:
        vehicle_style = ParagraphStyle(
            'VehicleInfo',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=10,
            alignment=0
        )
        vehicle_name = f"{vehicle['make']} {vehicle['model']} ({vehicle['year']})"
        elements.append(Paragraph(f"<b>{vehicle_name}</b>", vehicle_style))
        elements.append(Paragraph(f"<b>Type:</b> {vehicle['vehicle_type']} | <b>VIN:</b> {vehicle['vin']}", styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
    
    # Latest prediction
    if history:
        latest = history[0]
        elements.append(Paragraph("<b>Latest Prediction:</b>", styles['Heading3']))
        elements.append(Paragraph(f"Remaining KM: {latest['prediction_result']} km", styles['Normal']))
        elements.append(Paragraph(f"Range: {latest['prediction_range']}", styles['Normal']))
        elements.append(Paragraph(f"Date: {latest['created_at']}", styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
    
    # History table
    if history:
        elements.append(Paragraph("<b>Prediction History (Last 10):</b>", styles['Heading3']))
        data = [['Date', 'Remaining KM', 'Mileage', 'Temp', 'RPM']]
        for h in history[:10]:
            data.append([
                h['created_at'][:10],
                str(h['prediction_result']),
                str(int(h['mileage'])),
                str(h['engine_temp']),
                str(h['rpm'])
            ])
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#00c6ff')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Anomalies
    if anomalies:
        elements.append(PageBreak())
        elements.append(Paragraph("<b>Detected Anomalies:</b>", styles['Heading3']))
        for anomaly in anomalies:
            elements.append(Paragraph(f"• {anomaly['sensor_name']}: {anomaly['description']}", styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    
    doc.build(elements)
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, 
                     download_name=f'vehicle_report_{vehicle_id}.pdf')


# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    print(f"DEBUG SIGNUP: {username}")
    
    # Validate input
    if not username or not password:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"success": False, "error": "Username and password are required"}), 400
        return render_template('login.html', error="Username and password are required")
    
    try:
        db = sqlite3.connect('users.db')
        cursor = db.cursor()
        
        # Try to insert new user
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        
        # Get the newly created user's ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]
        db.close()
        
        # Log in the user after signup
        session["user"] = username
        session["user_id"] = user_id  # Store user_id for database queries
        
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"success": True, "redirect": url_for('home')}), 201
        return redirect(url_for('home'))
    
    except sqlite3.IntegrityError:
        # Username already exists
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"success": False, "error": "Username already exists"}), 409
        return render_template('login.html', error="Username already exists")
    except Exception as e:
        print(f"Signup error: {e}")
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"success": False, "error": "Signup error"}), 500
        return render_template('login.html', error="Signup error")


# ---------------- PREDICT ----------------
@app.route('/predict', methods=['POST'])
def predict():
    if "user" not in session or "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        user_id = session["user_id"]
        data = request.form  # ✅ important fix
        vehicle_id = request.form.get("vehicle_id")
        
        db = get_db()
        
        # If vehicle_id not provided, use the user's first vehicle
        if not vehicle_id:
            vehicle = db.execute(
                "SELECT id FROM vehicles WHERE user_id = ? LIMIT 1", 
                (user_id,)
            ).fetchone()
            
            if not vehicle:
                # If no vehicles exist, create a default one
                db.execute("""
                    INSERT INTO vehicles (user_id, vehicle_type, make, model, year)
                    VALUES (?, 'Car', 'Unknown', 'Unknown', 2020)
                """, (user_id,))
                db.commit()
                vehicle_id = db.execute(
                    "SELECT id FROM vehicles WHERE user_id = ? ORDER BY id DESC LIMIT 1",
                    (user_id,)
                ).fetchone()['id']
            else:
                vehicle_id = vehicle['id']
        else:
            # Verify that the provided vehicle_id belongs to the current user
            vehicle = db.execute(
                "SELECT user_id FROM vehicles WHERE id = ?", 
                (vehicle_id,)
            ).fetchone()
            if not vehicle or vehicle['user_id'] != user_id:
                db.close()
                return jsonify({"error": "Unauthorized"}), 403
        
        input_data = [
            vehicle_map.get(data.get("Vehicle_Type"), 0),
            float(data.get("Vehicle_Age", 0)),
            float(data.get("Mileage", 0)),
            float(data.get("Engine_Temp", 0)),
            float(data.get("RPM", 0)),
            float(data.get("Oil_Pressure", 0)),
            float(data.get("Fuel_Consumption", 0)),
            float(data.get("Battery_Voltage", 0)),
            float(data.get("Brake_Pressure", 0)),
            float(data.get("Tire_Pressure", 0)),
            tire_map.get(data.get("Tire_Condition"), 0),
            vibration_map.get(data.get("Vibration_Level"), 0),
            float(data.get("Last_Service_Months", 0)),
            accident_map.get(data.get("Accident_History"), 0),
        ]

        # Convert to numpy array with feature names if available
        if feature_names is not None:
            import pandas as pd
            input_df = pd.DataFrame([input_data], columns=feature_names)
            prediction = model.predict(input_df)[0]
        else:
            prediction = model.predict([input_data])[0]

        prediction_int = int(prediction)
        
        # Use new function to get both range and health status
        category_range, health_status = get_range_and_status(prediction_int)

        # Save to prediction history
        db.execute("""
            INSERT INTO prediction_history 
            (vehicle_id, vehicle_type, vehicle_age, mileage, engine_temp, rpm,
             oil_pressure, fuel_consumption, battery_voltage, brake_pressure,
             tire_pressure, tire_condition, vibration_level, last_service_months,
             accident_history, prediction_result, prediction_range)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            vehicle_id,
            data.get("Vehicle_Type"),
            float(data.get("Vehicle_Age", 0)),
            float(data.get("Mileage", 0)),
            float(data.get("Engine_Temp", 0)),
            float(data.get("RPM", 0)),
            float(data.get("Oil_Pressure", 0)),
            float(data.get("Fuel_Consumption", 0)),
            float(data.get("Battery_Voltage", 0)),
            float(data.get("Brake_Pressure", 0)),
            float(data.get("Tire_Pressure", 0)),
            data.get("Tire_Condition"),
            data.get("Vibration_Level"),
            float(data.get("Last_Service_Months", 0)),
            data.get("Accident_History"),
            prediction_int,
            category_range
        ))

        # Detect anomalies
        anomalies = detect_anomalies(data)
        for anomaly in anomalies:
            db.execute("""
                INSERT INTO anomalies 
                (vehicle_id, sensor_name, measured_value, normal_range_min, 
                 normal_range_max, alert_level, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                vehicle_id,
                anomaly['sensor'],
                anomaly['value'],
                anomaly['min'],
                anomaly['max'],
                anomaly['level'],
                anomaly['message']
            ))

        db.commit()
        db.close()

        return jsonify({
            "exact_pred": prediction_int,
            "range": category_range,  # renamed for clarity
            "health_status": health_status,
            "anomalies": anomalies,
            "anomaly_count": len(anomalies)
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, port=8000, use_reloader=True)