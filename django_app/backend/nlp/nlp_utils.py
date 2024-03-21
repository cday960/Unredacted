import io
import PyPDF2
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    CategoriesOptions,
    ConceptsOptions,
    KeywordsOptions,
    SummarizationOptions,
    EntitiesOptions
)

from .nlp_env import NLP_API_KEY, NLP_API_URL

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version="2022-04-07", authenticator=IAMAuthenticator(NLP_API_KEY)
)
natural_language_understanding.set_service_url(NLP_API_URL)

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


def nlp_analysis(text: str):
    response = None
    if len(text) > 0:
        response = natural_language_understanding.analyze(
            text=text,
            features=Features(
                entities=EntitiesOptions(sentiment=True, limit=30),
                categories=CategoriesOptions(limit=10),
                concepts=ConceptsOptions(limit=10),
                keywords=KeywordsOptions(limit=20),
                summarization = SummarizationOptions(limit=10)
            ),
        ).get_result()
        print(json.dumps(response, indent=2))
    return response


