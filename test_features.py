#!/usr/bin/env python3
"""
Test script for new features:
- Multi-vehicle management
- Prediction history
- Anomaly detection
- PDF export
"""

import requests
import json
from requests.Session import Session

BASE_URL = "http://localhost:5000"
session = requests.Session()

def test_login():
    """Test login"""
    print("Testing login...")
    response = session.post(f"{BASE_URL}/login", data={
        "username": "testuser",
        "password": "password123"
    })
    print(f"Login status: {response.status_code}")
    return response.status_code == 302 or response.status_code == 200

def test_add_vehicle():
    """Test adding a vehicle"""
    print("\nTesting add vehicle...")
    response = session.post(f"{BASE_URL}/vehicles", 
        json={
            "type": "Sedan",
            "make": "Toyota",
            "model": "Camry",
            "year": 2020,
            "vin": "ABC123DEF456"
        }
    )
    print(f"Add vehicle status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.status_code == 200

def test_get_vehicles():
    """Test getting vehicles"""
    print("\nTesting get vehicles...")
    response = session.get(f"{BASE_URL}/vehicles")
    print(f"Get vehicles status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.status_code == 200

def test_history():
    """Test getting history"""
    print("\nTesting get history...")
    response = session.get(f"{BASE_URL}/vehicle/1/history")
    print(f"Get history status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.status_code == 200

def test_anomalies():
    """Test getting anomalies"""
    print("\nTesting get anomalies...")
    response = session.get(f"{BASE_URL}/vehicle/1/anomalies")
    print(f"Get anomalies status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.status_code == 200

if __name__ == "__main__":
    print("Starting feature tests...\n")
    test_login()
    test_add_vehicle()
    test_get_vehicles()
    test_history()
    test_anomalies()
    print("\nTests completed!")
