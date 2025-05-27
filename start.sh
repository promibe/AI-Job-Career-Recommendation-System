#!/bin/bash

echo "Downloading model..."
python download_model.py

echo "Starting FastAPI..."
uvicorn app:app #--host 0.0.0.0 --port 8000 &

echo "Starting Streamlit..."
streamlit run frontend/frontend.py #--server.port 8501 --server.address 0.0.0.0