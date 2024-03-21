from models import Document, DigitalObject
from atlas.utils.db import mongo_db
from atlas.utils.na_api import na_api
from atlas.utils.nlp import nlp
from .doc_processing import process_doc

def load_doc(naId: int):
    # first check if already in the database
    # if so, retrieve
    # else, run it through NLP
    # then add to database
    # deliver doc

    doc: Document = mongo_db.get_doc(naId)

    if doc is not None:
        print(f"Retrieved {doc.filename} from db.")
    else:
        doc = process_doc(doc)

    return doc

def get_recent_docs(num_docs: int = 10) -> list[Document]:
    doc_list = mongo_db.get_recent_docs(num_docs)
    return doc_list


def get_doc(naId: int) -> Document:
    doc = mongo_db.get_doc(naId)
    return doc


def get_search_results(query: str) -> list[Document]:
    doc_list = []

    # check db first
    docs_from_db = mongo_db.query_db(query)
    doc_list.extend(docs_from_db)

    # if there wasn't many from the db, get from the NA
    if len(docs_from_db) < 5:
        
        # get the docs from the NA
        docs_from_na = na_api.query_pdf_documents(q=query)

        for doc in docs_from_na:
            doc = process_doc(doc)

        doc_list.extend(docs_from_na)
    
    return doc_list
