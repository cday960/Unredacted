from decouple import config
import io
import PyPDF2
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    CategoriesOptions,
    ConceptsOptions,
    KeywordsOptions,
)


# NLP_API_KEY = config("NLP_API_KEY")
# NLP_API_URL = config("NLP_API_URL")
# SAMPLE_TEXT_TO_ANALYZE = ""

# with open("NLP/SAMPLE_TEXT.txt", "r") as file:
#     text = " ".join(line.rstrip() for line in file)
#     SAMPLE_TEXT_TO_ANALYZE = text

# authenticator = IAMAuthenticator(NLP_API_KEY)
# natural_language_understanding = NaturalLanguageUnderstandingV1(
#     version="2022-04-07", authenticator=authenticator
# )

# natural_language_understanding.set_service_url(NLP_API_URL)

# response = natural_language_understanding.analyze(
#     text=SAMPLE_TEXT_TO_ANALYZE,
#     features=Features(
#         entities=EntitiesOptions(sentiment=True, limit=30),
#         categories=CategoriesOptions(limit=10),
#         concepts=ConceptsOptions(limit=10),
#         keywords=KeywordsOptions(limit=20),
#     ),
# ).get_result()

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

def summarize_pdf(pdf: bytes):
    pdf_text = extract_pdf_text(pdf)
    '''
    ADD SUMMARY HERE!!!
    '''
    return pdf_text