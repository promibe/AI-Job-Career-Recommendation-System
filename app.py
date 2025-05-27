from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
from models.predictor import process_resume

app = FastAPI()

@app.post("/analyze_resume_file/")
async def analyze_resume_file(file: UploadFile = File(...)):
    temp_path = f"temp_files/{file.filename}"
    os.makedirs("temp_files", exist_ok=True)

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    result = process_resume(temp_path)
    os.remove(temp_path)

    return JSONResponse(content=result)