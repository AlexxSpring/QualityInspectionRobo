#!/bin/bash

echo "Starting Quality Inspection Dashboard Setup..."

# Check if .venv exists, if not, create it
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv .venv
    
    echo "Activating virtual environment..."
    source .venv/bin/activate
    
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Activating existing virtual environment..."
    source .venv/bin/activate
fi

echo "Starting Uvicorn Server..."
export PYTHONPATH=$(pwd)
uvicorn app.main:app --host 0.0.0.0 --port 8000
