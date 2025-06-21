import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Extracts text from all pages of a PDF file using pdfplumber."""
    extracted_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n\n"  # Adding spacing for better readability
    return extracted_text.strip()  # Remove extra spaces at the end
