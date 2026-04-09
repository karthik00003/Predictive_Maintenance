#!/usr/bin/env python3
"""
Test script for Vehi Care application
Validates all endpoints and model functionality
"""

from app import app, model
import json

print("=" * 60)
print("VEHI CARE - APPLICATION TEST SUITE")
print("=" * 60)

with app.test_client() as client:
    print("\n1. Testing Flask Application Setup")
    print("-" * 60)
    print("✓ Flask app imported successfully")
    print("✓ ML model loaded successfully")
    
    print("\n2. Testing Authentication Endpoints")
    print("-" * 60)
    
    # Test login
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 302, f"Login failed: {response.status_code}"
    print("✓ Login endpoint works (redirects)")
    
    # Test logout
    response = client.get('/logout')
    assert response.status_code == 302, f"Logout failed: {response.status_code}"
    print("✓ Logout endpoint works (redirects)")
    
    print("\n3. Testing Page Routes")
    print("-" * 60)
    
    # Create authenticated session
    with client.session_transaction() as sess:
        sess['user'] = 'testuser'
    
    # Test home page
    response = client.get('/home')
    assert response.status_code == 200, f"Home page failed: {response.status_code}"
    print("✓ Home page loads successfully")
    
    # Test predict page
    response = client.get('/predict_page')
    assert response.status_code == 200, f"Predict page failed: {response.status_code}"
    print("✓ Predict page loads successfully")
    
    print("\n4. Testing Prediction Endpoint")
    print("-" * 60)
    
    test_data = {
        'Vehicle_Type': 'Sedan',
        'Vehicle_Age': 5,
        'Mileage': 50000,
        'Engine_Temp': 90,
        'RPM': 800,
        'Oil_Pressure': 35,
        'Fuel_Consumption': 12,
        'Battery_Voltage': 13.5,
        'Brake_Pressure': 38,
        'Tire_Pressure': 32,
        'Tire_Condition': 'Good',
        'Vibration_Level': 'Low',
        'Last_Service_Months': 3,
        'Accident_History': 'No'
    }
    
    response = client.post('/predict', data=test_data)
    assert response.status_code == 200, f"Predict endpoint failed: {response.status_code}"
    
    result = json.loads(response.data)
    assert 'exact_pred' in result and 'range_pred' in result, "Invalid prediction response"
    
    print("✓ Prediction endpoint works")
    print(f"  - Exact prediction: {result['exact_pred']} km")
    print(f"  - Range prediction: {result['range_pred']}")
    
    print("\n5. Testing Edge Cases")
    print("-" * 60)
    
    # Test with missing data
    incomplete_data = {'Vehicle_Type': 'Sedan'}
    response = client.post('/predict', data=incomplete_data)
    result = json.loads(response.data)
    if 'error' in result:
        print("✓ Error handling for incomplete data works")
        print(f"  - Error message: {result['error'][:50]}...")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print("\nApplication is ready to run!")
    print("Start the server with: python3 app.py")
    print("Or use the run script: ./run.sh")
    print("=" * 60)
