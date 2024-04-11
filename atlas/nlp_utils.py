import os
from dotenv import load_dotenv
import threading
import time
from doc_models import Document, DocQueue, Keywords
from mongo_db import mongo_db
from na_api import na_api
import io
import PyPDF2
import json
import time
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    CategoriesOptions,
    ConceptsOptions,
    KeywordsOptions,
    SummarizationOptions,
    EntitiesOptions,
)

load_dotenv()

NLP_API_KEY = str(os.getenv("NLP_API_KEY"))
NLP_API_URL = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/1645185e-ee50-492f-b1f3-5093f5094d51"

print(f"Watson API Key: {NLP_API_KEY}")


natural_language_understanding = NaturalLanguageUnderstandingV1(
    version="2022-04-07", authenticator=IAMAuthenticator(NLP_API_KEY)
)
natural_language_understanding.set_service_url(NLP_API_URL)


# background processing daemon
doc_queue = DocQueue()


def keep_processing_docs(doc_queue: DocQueue):
    while True:
        doc: Document = doc_queue.dequeue()
        if doc is not None:
            doc = process_doc(doc)
        time.sleep(1)


def start_doc_processing():
    processing_thread = threading.Thread(
        target=keep_processing_docs, args=(doc_queue,), daemon=True
    )
    processing_thread.start()
    print("Started NLP processing thread.")


def queue_doc_for_processing(doc: Document):
    doc_queue.enqueue(doc)


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
                summarization=SummarizationOptions(limit=10),
            ),
        ).get_result()
        print(json.dumps(response, indent=2))
    return response


def process_doc(doc: Document) -> Document:
    for digitalObject in doc.digitalObjects:
        pdf_bytes = na_api.get_raw_na_url(digitalObject.url).content
        extracted_text = extract_pdf_text(pdf_bytes)
        nlp_stuff = nlp_analysis(extracted_text)
        if nlp_stuff is not None:
            doc.keywords = [Keywords(raw_json=key) for key in nlp_stuff["keywords"]]
            digitalObject.summary = nlp_stuff["summarization"]["text"]
    mongo_db.insert_doc(doc)
    return doc
