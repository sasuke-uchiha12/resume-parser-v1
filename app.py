import re
import spacy
from pdfminer.high_level import extract_text

# Load SpaCy's English language model
nlp = spacy.load("en_core_web_sm")

# Function to read PDF resumes
def read_pdf(file_path):
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

# Function to process the text with SpaCy
def process_text(text):
    doc = nlp(text)
    return doc

# Function to extract email addresses
def extract_email(doc):
    emails = []
    for token in doc:
        if token.like_email:
            emails.append(token.text)
    return emails

# Function to extract phone numbers
def extract_phone(doc):
    phone_numbers = []
    phone_regex = r'\+?1?\d{9,15}'  # Simple phone number regex
    for token in doc:
        if re.match(phone_regex, token.text):
            phone_numbers.append(token.text)
    return phone_numbers

# Function to extract names
def extract_name(doc):
    names = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            names.append(ent.text)
    return names

# Function to parse a resume and extract relevant information
def parse_resume(file_path):
    text = read_pdf(file_path)
    if not text:  # If text extraction fails
        return {}
    
    doc = process_text(text)
    
    resume_data = {
        'name': extract_name(doc),
        'email': extract_email(doc),
        'phone': extract_phone(doc),
    }
    
    return resume_data

# Main function to run the parser
if __name__ == "__main__":
    # Specify the path to your resume PDF file here
    file_path = 'resume/resume_v4.pdf'
    
    # Parse the resume
    resume_info = parse_resume(file_path)
    
    # Print extracted information
    print("Extracted Resume Information:")
    print(resume_info)
