#!/bin/bash

cd "$(dirname "$0")"

echo "Starting Quality Inspection Dashboard Setup..."

if [ ! -d ".venv" ]; then
python3 -m venv .venv --system-site-packages
fi

echo "Activating virtual environment..."
source .venv/bin/activate

# 🔥 Correct place

export GPIOZERO_PIN_FACTORY=lgpio

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting Uvicorn Server..."
export PYTHONPATH=$(pwd)
uvicorn app.main:app --host 0.0.0.0 --port 8000

