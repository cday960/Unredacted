from models import Document
from db import mongo_db
from na_api import na_api
from nlp import nlp


def process_doc(doc: Document) -> Document:
    for digitalObject in doc.digitalObjects:
            pdf_bytes = na_api.get_pdf_from_na(digitalObject.url)
            extracted_text = nlp.extract_pdf_text(pdf_bytes)
            digitalObject.description = extracted_text
            digitalObject.summary = nlp.summarize_pdf(extracted_text)
            
    mongo_db.insert_doc(doc)
    return doc