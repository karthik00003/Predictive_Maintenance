#!/bin/bash

# Script to run the Vehi Care application

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Starting Flask server..."
echo "App will be available at: http://127.0.0.1:5000"
echo ""

python3 app.py
