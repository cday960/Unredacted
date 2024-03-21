import os
import json
import requests

from typing import Any
from flask import Blueprint, jsonify
from dotenv import load_dotenv
from models import Document

from util.search import na_id_search
from models import Document, DigitalObject, DocQueue
from utils import mongo_db, na_api, start_nlp_processing

webapp = Blueprint("webapp", __name__, url_prefix="/webapp")

load_dotenv()

api_url = "https://catalog.archives.gov/api/v2/"
api_key = str(os.getenv("API_KEY"))
headers = {"Content-Type": "application/json", "x-api-key": api_key}

dq = DocQueue()

start_nlp_processing(dq)


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


@webapp.route("/search/<string:search_parameters>?<int:result_limit>", methods=["GET"])
@webapp.route("/search/<string:search_parameters>", methods=["GET"])
def webapp_search(search_parameters: str, result_limit: int = 20):
    """
    127.0.0.1:5000/webapp/search/<search_parameters>
    Example: 127.0.0.1:5000/webapp/search/john+f+kennedy
        + acts as a space in a url
    """

    if search_parameters is None:
        return jsonify({"error": "invalid search parameters given"}), 400
    
    doc_list = []

    # query: dict[str, Any] = {'keywords': search_paramters.split('+')}

    # check db first
    query: dict[str, Any] = {}
    docs_from_db = mongo_db.query_db(query)
    doc_list.extend(docs_from_db)

    # if there wasn't many from the db, get from the NA
    if len(docs_from_db) < 5:
        
        # get the docs from the NA
        docs_from_na = na_api.query_pdf_documents(q=search_parameters, limit=result_limit)

        for doc in docs_from_na:
            dq.enqueue(doc)

        doc_list.extend(docs_from_na)

    return jsonify({"data": doc_list[0:result_limit]})


@webapp.route("/record/id/<int:naId>", methods=["GET"])
@webapp.route("/record/id/<int:naId>?<int:uuid>", methods=["GET"])
def webapp_records(naId: int, uuid: int = ""):
    if naId is None:
        return jsonify({"error": "invalid naId parameters given"}), 400
    
    doc = get_doc(naId)

    return jsonify({"data": doc.to_dict()})


@webapp.route("/recent", methods=["GET"])
def webapp_recent():
    
    doc_list = mongo_db.get_recent_docs()

    return jsonify({"data": doc_list})


@webapp.route("/pdf/id/<int:naId>?<int:do_index>", methods=["GET"])
def webapp_records(naId: int, do_index: int = ""):
    if naId is None:
        return jsonify({"error": "invalid naId parameters given"}), 400
    
    if do_index is None:
        do_index = 0
    
    doc = get_doc(naId)

    try:
        do: DigitalObject = doc.digitalObjects[do_index]
        na_response = na_api.get_raw_na_url(do.url)
    except IndexError:
        return jsonify({"error": "invalid digitalObject index given"}), 400
    
    return jsonify({"data": na_response})