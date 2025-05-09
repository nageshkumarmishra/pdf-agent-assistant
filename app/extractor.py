# --- app/extractor.py ---
# Handles text extraction from PDF files using PyPDF2

from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    """
    Extracts and returns the combined text from all pages of a PDF file.
    """
    try:
        reader = PdfReader(file_path)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    except Exception as e:
        raise RuntimeError(f"Error extracting text from PDF: {str(e)}")
