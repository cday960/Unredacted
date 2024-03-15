import os

from flask import Blueprint, jsonify
from dotenv import load_dotenv
from models import Document
from util.search import na_id_search

nlp = Blueprint("nlp", __name__, url_prefix="/nlp")

load_dotenv()

api_url = "https://catalog.archives.gov/api/v2/"
api_key = str(os.getenv("API_KEY"))
headers = {"Content-Type": "application/json", "x-api-key": api_key}


@nlp.route("/record/<string:naId>", methods=["GET"])
def webapp_to_nlp(naId: str):
    """
    Tentatively this takes an ID and then sends it to the NLP.

    Right now, this does the same thing as /webapp/records/id, but in the future
    it will check the database to see if the document has already been processed, and
    if not it is sent to the NLP.
    """
    doc = na_id_search(naId)

    """
    # 0 meaning the document is NOT in the database
    if document_db_check(doc) != 0:
        nlp_url = "http://nlp"
        data = doc.to_json()
        nlp_response = requests.post(nlp_url, json=data)
        doc_to_db(doc)  # sends the document to the DB
        return jsonify({"data": nlp_response})
    else:
        nlp_analysis = db_id_search(naId)
        return jsonify({"data": nlp_analysis})
    """

    return jsonify({"data": doc.to_dict()})


def document_db_check(doc: Document) -> int:
    """
    Will check the database to see if the document is in the database
    and processed
    """
    return 1
