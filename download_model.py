# download_model.py
import gdown
import os
from dotenv import load_dotenv


# Load environment variables from .env if available
load_dotenv()

output_path = "models/saved_model_classifier/model.safetensors"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

file_id = os.getenv("MODEL_FILE_ID")
if not file_id:
    raise ValueError("Environment variable MODEL_FILE_ID not set.")

url = f"https://drive.google.com/uc?id={file_id}"

if os.path.exists(output_path):
    print("Model already downloaded, skipping download.")
else:
    gdown.download(url, output_path, quiet=False)
