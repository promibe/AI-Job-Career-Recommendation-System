import re

def clean_text(text):
    """
    Cleans raw resume text for BERT input:
    - Removes URLs, emails, and extra spaces
    - Converts to lowercase
    - Removes special characters
    """
    if not isinstance(text, str):
        return ""

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)

    # Remove emails
    text = re.sub(r'\S+@\S+', '', text)

    # Remove newlines, tabs, and extra spaces
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    text = re.sub(' +', ' ', text)

    # Remove unwanted special characters (retain common punctuation)
    text = re.sub(r"[^a-zA-Z0-9.,!?()\- ]", '', text)

    # Convert to lowercase
    return text.lower().strip()
