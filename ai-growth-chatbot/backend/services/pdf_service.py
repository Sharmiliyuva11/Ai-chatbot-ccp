import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return {"success": True, "text": text.strip()}
    except Exception as e:
        return {"success": False, "error": str(e)}
