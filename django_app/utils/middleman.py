from doc_models import Document, DigitalObject
from .db_interaction import MongoDb
from .na_search import get_doc_from_na, get_pdf_from_na
from .nlp import summarize_pdf, extract_pdf_text

db = MongoDb()


def load_doc(naId: int):
    # first check if already in the database
    # if so, retrieve
    # else, run it through NLP
    # then add to database
    # deliver doc

    doc: Document = db.get_doc(naId)

    if doc is not None:
        print(f"Retrieved {doc.filename} from db.")
    else:
        doc = get_doc_from_na(naId)

        for digitalObject in doc.digitalObjects:
            pdf_bytes = get_pdf_from_na(digitalObject.url)
            extracted_text = extract_pdf_text(pdf_bytes)
            digitalObject.description = extracted_text
            digitalObject.summary = summarize_pdf(extracted_text)

        db.insert_doc(doc)

    return doc

def get_recent_docs(num_docs: int = 10) -> list[Document]:
    doc_list = db.get_recent_docs(num_docs)
    return doc_list
