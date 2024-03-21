import io
import PyPDF2

def extract_pdf_text(pdf_bytes: bytes):
    # Create a file-like object from the PDF bytes
    pdf_file = io.BytesIO(pdf_bytes)

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Initialize an empty text variable
    text = ""

    # Extract text from each page and append to the text variable
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    return text
