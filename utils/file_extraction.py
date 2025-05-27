import os
import pymupdf  # fitz
from docx import Document

def extract_text_from_pdf(pdf_path):
    full_text = ""
    try:
        with pymupdf.open(pdf_path) as doc:
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
        raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")

