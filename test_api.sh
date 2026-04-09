#!/bin/bash

echo "Testing Vehi Care API Endpoints..."
echo ""

# Test 1: Get root (should redirect to login)
echo "Test 1: GET / (should show login page)"
curl -s -w "\nStatus: %{http_code}\n" http://localhost:5000/ | head -5
echo ""

# Test 2: Access vehicles endpoint without login (should redirect)
echo "Test 2: GET /vehicles without auth (should redirect)"
curl -s -w "\nStatus: %{http_code}\n" http://localhost:5000/vehicles 
echo ""

# Test 3: Test login with curl
echo "Test 3: POST /login"
curl -s -c /tmp/cookies.txt -X POST \
  -d "username=testuser&password=password123" \
  http://localhost:5000/login
echo ""

# Test 4: Try vehicles with session cookie
echo "Test 4: GET /vehicles with session"
curl -s -b /tmp/cookies.txt http://localhost:5000/vehicles | head -20
echo ""

# Test 5: Create a vehicle
echo "Test 5: POST /vehicles (add vehicle)"
curl -s -b /tmp/cookies.txt \
  -H "Content-Type: application/json" \
  -d '{"type":"Sedan","make":"Toyota","model":"Camry","year":2020,"vin":"ABC123"}' \
  http://localhost:5000/vehicles | head -20
echo ""

echo "Test suite completed!"
