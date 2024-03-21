from typing import Any

from doc_models import Document, DocQueue
from .db import mongo_db
from .na_api import na_api
from .nlp import start_nlp_processing

dq = DocQueue()

start_nlp_processing(dq)

def doc_list_check(doc: Document, doc_list: list[Document]):
    for d in doc_list:
        if doc.naId == d.naId:
            return True
    return False

def get_docs(search_params: str, result_limit: int = 20):

    doc_list = []

    # query: dict[str, Any] = {'keywords': search_paramters.split('+')}

    # check db first
    query: dict[str, Any] = {}
    # docs_from_db = mongo_db.query_db(query)
    docs_from_db = []
    doc_list.extend(docs_from_db)

    # if there wasn't many from the db, get from the NA
    if len(docs_from_db) < 10:
        # get the docs from the NA
        docs_from_na = na_api.query_pdf_documents(q=search_params, limit=result_limit)

        for doc in docs_from_na:
            if not doc_list_check(doc, docs_from_db):
                dq.enqueue(doc)
                doc_list.append(doc)
    
    return doc_list


def get_doc(naId: int) -> Document:
    doc: Document = mongo_db.get_doc(naId)

    if doc is not None:
        print(f"Retrieved {doc.filename} from db.")
    else:
        doc: Document = na_api.get_doc_from_na(naId)
        if doc is not None:
            dq.enqueue(doc)
        else: 
            raise RuntimeError(f"Document could not be found with {naId}!")

    return doc


def get_pdf(url: str):
    return na_api.get_raw_na_url(url).content

def get_recent_docs(num_docs: int = 5):
    return mongo_db.get_recent_docs()[:num_docs]