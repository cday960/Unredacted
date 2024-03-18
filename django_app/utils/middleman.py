from ibm_cloud_sdk_core.base_service import requests
from doc_models import Document, DigitalObject
from .db_interaction import db_get_doc, db_insert_doc
from .nlp import summarize_pdf
import os

NA_API_KEY = str(os.getenv("NA_API_KEY"))
headers = {"Content-Type": "application/json", "x-api-key": NA_API_KEY}
atlas_url = "http://127.0.0.1:5000"


def load_doc(naId: int) -> Document:
    # first check if already in the database
    # if so, retrieve
    # else, run it through NLP
    # then add to database
    # deliver doc

    # doc: Document = None

    json_response = db_get_doc(naId)

    if json_response[0] != 0:
        # just give the doc back
        doc = json_response[1]
        print("Retrieved!")
        print(json_response)
    else:
        url = f"{atlas_url}/webapp/record/id/{naId}"
        json_response = requests.get(url, headers).json()["data"][0]

        doc = Document(raw_json=json_response)

        for digitalObject in doc.digitalObjects:
            summary = summarize_pdf(requests.get(digitalObject.url, headers).content)
            digitalObject.summary = summary

        db_insert_doc(doc)

    return doc
