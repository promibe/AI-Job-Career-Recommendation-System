import os
import torch
import json
import pandas as pd
from transformers import AutoTokenizer, BertForSequenceClassification
from fuzzywuzzy import fuzz
from utils.file_extraction import extract_resume_text
from utils.text_cleaning import clean_text
from utils.skill_matcher import extract_skills

# Load model/tokenizer/label names once
model_dir = "models/saved_resume_classifier"
model = BertForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)
label_names = list(pd.read_csv('data/encode_label.csv')['0'])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

with open('data/skill_gap.json', 'r') as f:
    skill_gap_data = json.load(f)

def process_resume(file_path):
    raw_text = extract_resume_text(file_path)
    if not raw_text:
        return {"error": "Could not extract text"}

    cleaned_text = clean_text(raw_text)

    # Predict job category
    inputs = tokenizer(cleaned_text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=1)
    pred_idx = torch.argmax(probs, dim=1).item()

    predicted_label = label_names[pred_idx]
    confidence = probs[0][pred_idx].item()

    # Skill gap analysis
    required_skills = skill_gap_data.get(predicted_label, [])
    matched, missing, percentage_gap = extract_skills(cleaned_text, required_skills)

    status = "Take for Interview" if percentage_gap >= 50 else "Not Qualified"

    return {
        "predicted_role": predicted_label,
        #"confidence": round(confidence * 100, 2),
        "certified_skills": matched,
        "missing_skills": missing,
        "skill_gap_percentage": round(100 - percentage_gap, 2),
        "status": status
    }


    
