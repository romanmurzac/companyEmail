import PyPDF2


def extract_pdf_content(pdf_path: str) -> str:
    reader = PyPDF2.PdfReader(pdf_path)
    pdf_data = reader.pages[0].extract_text()
    return pdf_data
