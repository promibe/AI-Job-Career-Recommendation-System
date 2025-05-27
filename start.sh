#!/bin/bash

echo "Downloading model..."
python download_model.py

echo "Starting your app..."
python app.py  # Replace with uvicorn main:app --host 0.0.0.0 --port 10000 if needed
