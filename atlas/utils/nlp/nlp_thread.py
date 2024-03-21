import threading
import time
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    CategoriesOptions,
    ConceptsOptions,
    KeywordsOptions,
)
from models import Document, DocQueue
from .nlp_env import NLP_API_KEY, NLP_API_URL
from .nlp_utils import extract_pdf_text
from db import mongo_db
from na_api import na_api

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version="2022-04-07", authenticator=IAMAuthenticator(NLP_API_KEY)
)
natural_language_understanding.set_service_url(NLP_API_URL)


def process_docs(doc_queue: DocQueue):
    while True:
        doc = doc_queue.dequeue()
        if doc is not None:
            for digitalObject in doc.digitalObjects:
                pdf_bytes = na_api.get_raw_na_url(digitalObject.url).content
                extracted_text = extract_pdf_text(pdf_bytes)
                digitalObject.description = extracted_text
                
            mongo_db.insert_doc(doc)
        time.sleep(1)


def start_nlp_processing(doc_queue: DocQueue):
    processing_thread = threading.Thread(target=process_docs, args=(doc_queue,), daemon=True)
    processing_thread.start()

