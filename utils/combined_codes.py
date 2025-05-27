# import the necessary libaries to enable the loading of the resume, whether in doc or pdf format
import pymupdf
from docx import Document
import os
import re
from transformers import AutoTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer
import json
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer, util
import pandas as pd


# ====================================== file path =======================================================

file_path = r'training_datasets\AI-powered-career-guidance-project-dataset\data\ACCOUNTANT\10554236.pdf'

# ========================================================================================================

# ======================================= Extracting functions ===========================================

#creating a function to extract the text in the pdf
def extract_text_from_pdf(pdf_path):
    full_text = ""
    try:
        with pymupdf.open(pdf_path) as doc:
          for page in doc:
              full_text = "\n".join([page.get_text() for page in doc])
    except Exception as e:
        print(f"Failed to read PDF {pdf_path}: {e}")
    return full_text


def extract_text_from_docx(docx_path):
    text = ""
    try:
        doc = Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Failed to read DOCX {docx_path}: {e}")
    return text


def extract_resume_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        return None  # unsupported file type
    

text = extract_resume_text(file_path=file_path)

# ==========================================================================================

# ============================================= Preprocessing (cleaning) function ===========================
def clean_text(text):
    """
    Cleans raw resume text for BERT input.
    - Removes URLs, special characters, and extra spaces
    - Converts to lowercase
    """

    if not isinstance(text, str):
        return ""  # or np.nan if you want to track missing

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)

    # Remove emails
    text = re.sub(r'\S+@\S+', '', text)

    # Remove newline, tab, and multiple spaces
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    text = re.sub(' +', ' ', text)

    # Remove special characters (except alphanumerics and basic punctuation)
    text = re.sub(r"[^a-zA-Z0-9.,!?()\- ]", '', text)

    # Lowercase the text
    text = text.lower()

    return text.strip()

clean_text = clean_text(text)
# ==================================================================================================

# ================================= Loading the model ==============================================
save_directory = r"models\saved_resume_classifier"

# ===================== 1. loading the model and tokenizer ===========================================
model = BertForSequenceClassification.from_pretrained(save_directory)
tokenizer = AutoTokenizer.from_pretrained(save_directory)

# Detect device (GPU if available, else CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# =================== loading the label names ======================================================

label_names = list(pd.read_csv(r'data\encode_label.csv')['0'])


# ===================== Defining the prediction function ===========================================

def predict_resume(text, model, tokenizer, label_names):
    # Tokenize inputs and move to the same device as model
    inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=1)
    pred_idx = torch.argmax(probs, dim=1).item()
    return label_names[pred_idx], probs[0][pred_idx].item()


predicted_label, confidence = predict_resume(clean_text, model, tokenizer, label_names)
print(f"Predicted label: {predicted_label})")


# ======================================================================================================

# ============================================= SKILL GAP MATCHING =====================================


skill_gap_file_path = r'data\skill_gap.json'

with open(skill_gap_file_path, 'r') as file:
    skill_gap_data = json.load(file)

## applying exact skill matching
# from the required skill and the ones in the resume i want to create a percentage value for skill gap
from fuzzywuzzy import fuzz

def extract_skills(resume_text, skill_set, fuzzy_threshold=90):
    resume_text = resume_text.lower()
    matched_skills = set()

    for skill in skill_set:
        # Exact match
        if skill.lower() in resume_text:
            matched_skills.add(skill)
        else:
            # Fuzzy match if not found
            ratio = fuzz.partial_ratio(skill.lower(), resume_text)
            if ratio >= fuzzy_threshold:
                matched_skills.add(skill)

    #selecting the skills that are not in the matched_skills
    remaining_skills = [skill for skill in skill_set if skill not in matched_skills]

    #percentage value for skill gap
    percentage_gap = (len(matched_skills) / len(skill_set)) * 100


    return sorted(list(matched_skills)), remaining_skills, percentage_gap



if predicted_label:
    
    #print(skill_gap_data.keys())
    
    certified_required_skills, skill_gap, percentage_gap = extract_skills(clean_text, skill_gap_data[predicted_label])

    status = None
    if percentage_gap < 50:
        status = 'Not Qualified'
    else:
        status = 'Take for Interview' 

    Name = input('Enter Your Name: ')
    Email = input('Enter Your Email Address: ')

    print(f'''
        Hello!
        A resume has been analyzed-
        Name: {Name}
        Email: {Email}
        Suggested role: {predicted_label}
        Certified Required skills: {', '.join(certified_required_skills)}
        skill gap: {', '.join(skill_gap)}
        User has {percentage_gap}% skill gap
        {status}
          ''')
