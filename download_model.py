# download_model.py
import gdown
import os

output_path = "model/saved_model_classifier/model.safetensors"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

file_id = "185uEtDKfV7kYRfGCLL7LYiF5zF1KmoNv"  # replace with your real ID
url = f"https://drive.google.com/uc?id={file_id}"

if os.path.exists(output_path):
    print("Model already downloaded, skipping download.")
else:
    gdown.download(url, output_path, quiet=False)
