import fitz  # PyMuPDF

def parse_resume_text(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        text = "Error reading resume: " + str(e)
    return text
