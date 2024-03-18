from doc_models import Document, DigitalObject
from .db_interaction import db_get_doc, db_insert_doc
from .na_search import get_doc_from_na, get_pdf_from_na
from .nlp import summarize_pdf


def load_doc(naId: int):
    # first check if already in the database
    # if so, retrieve
    # else, run it through NLP
    # then add to database
    # deliver doc

    doc: Document = db_get_doc(naId)

    if doc is not None:
        print(f"Retrieved {doc.filename} from db.")
    else:
        doc = get_doc_from_na(naId)

        for digitalObject in doc.digitalObjects:
            digitalObject.summary = summarize_pdf(get_pdf_from_na(digitalObject.url))

        db_insert_doc(doc)
        
        

    return doc