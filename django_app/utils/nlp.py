import io
import os
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

NLP_API_KEY = str(os.getenv("NLP_API_KEY"))
NLP_API_URL = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/1645185e-ee50-492f-b1f3-5093f5094d51"

print(f"National Archives API Key: {NLP_API_KEY}")

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version="2022-04-07", authenticator=IAMAuthenticator(NLP_API_KEY)
)
natural_language_understanding.set_service_url(NLP_API_URL)

# SAMPLE_TEXT_TO_ANALYZE = ""
# with open("NLP/SAMPLE_TEXT.txt", "r") as file:
#     text = " ".join(line.rstrip() for line in file)
#     SAMPLE_TEXT_TO_ANALYZE = text

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

def summarize_pdf(text: str):
    if len(text) > 0:
        response = natural_language_understanding.analyze(
            text=text,
            features=Features(
                entities=EntitiesOptions(sentiment=True, limit=30),
                categories=CategoriesOptions(limit=10),
                concepts=ConceptsOptions(limit=10),
                keywords=KeywordsOptions(limit=20),
            ),
        ).get_result()
        print(response)
    return None