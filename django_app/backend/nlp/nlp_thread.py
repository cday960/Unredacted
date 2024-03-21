import threading
import json
import time
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    CategoriesOptions,
    ConceptsOptions,
    KeywordsOptions,
    SummarizationOptions,
)
from doc_models import Document, DocQueue
from .nlp_utils import extract_pdf_text, nlp_analysis
from backend.db import mongo_db
from backend.na_api import na_api

def process_docs(doc_queue: DocQueue):
    while True:
        doc: Document = doc_queue.dequeue()
        if doc is not None:
            for digitalObject in doc.digitalObjects:
                pdf_bytes = na_api.get_raw_na_url(digitalObject.url).content
                extracted_text = extract_pdf_text(pdf_bytes)
                nlp_stuff = nlp_analysis(extracted_text)
                try:
                    digitalObject.description = json.dumps(nlp_stuff['keywords'], indent=2)
                    digitalObject.summary = nlp_stuff['summarization']['text']
                except (KeyError, TypeError):
                    pass
                
            mongo_db.insert_doc(doc)
        time.sleep(1)


def start_nlp_processing(doc_queue: DocQueue):
    processing_thread = threading.Thread(target=process_docs, args=(doc_queue,), daemon=True)
    processing_thread.start()
    print("Started NLP processing thread.")

