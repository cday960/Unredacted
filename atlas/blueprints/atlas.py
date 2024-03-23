from typing import Any
from flask import Flask, Blueprint, jsonify, request, Response
from doc_models import Document
from mongo_db import mongo_db
from na_api import na_api
from nlp_utils import process_doc, queue_doc_for_processing


atlas = Blueprint("atlas", __name__, url_prefix="/atlas")


# @atlas.route("/process", methods=["POST"])
# def process_doc_raw():

#     doc = Document(raw_json=request.document)

#     if doc is not None:
#         doc = process_doc(doc)
#     else:
#         return jsonify({"error": f"Document JSON not provided."}), 400

#     return jsonify({"data": doc.to_dict()}), 200


@atlas.route("/process/<int:naId>", methods=["GET"])
def process_doc_naid(naId: int):

    if naId is None:
        return jsonify({"error": "invalid naId parameters given"}), 400

    doc: Document = mongo_db.get_doc(naId)
    
    if doc is not None:
        print(f"Retrieved {doc.filename} from db.")
    else:
        doc: Document = na_api.get_doc_from_na(naId)
        if doc is not None:
            doc = process_doc(doc)
        else:
            return jsonify({"error": f"Document not in National Archives"}), 400
      
    return jsonify({"data": doc.to_dict()}), 200


@atlas.route("/query/<string:search_parameters>?<int:result_limit>", methods=["GET"])
@atlas.route("/query/<string:search_parameters>", methods=["GET"])
def search_docs(search_parameters: str, result_limit: int = 20):
    """
    127.0.0.1:5000/webapp/search/<search_parameters>
    Example: 127.0.0.1:5000/webapp/search/john+f+kennedy
        + acts as a space in a url
    """

    if search_parameters is None:
        return jsonify({"error": "invalid search parameters given"}), 400

    doc_list: list[Document] = []

    # check db first
    docs_from_db: list[Document] = mongo_db.keyword_search(search_parameters.split('+'))
    doc_list.extend(docs_from_db)

    # if there wasn't many from the db, get from the NA
    if len(docs_from_db) < 5:

        # get the docs from the NA
        docs_from_na: list[Document] = na_api.query_pdf_documents(
            q=search_parameters, limit=result_limit
        )

        # start processing on each one -> grow database
        for doc in docs_from_na:
            queue_doc_for_processing(doc)

        doc_list.extend(docs_from_na)

    

    return jsonify({"data": [doc.to_dict() for doc in doc_list]}), 200


@atlas.route("/recent/<int:result_limit>", methods=["GET"])
def recent_docs(result_limit: int = 10):
    recent_docs: list[Document] = mongo_db.get_recent_docs(result_limit)
    return jsonify({"data": recent_docs})


@atlas.route("/pdf/<path:url>", methods=["GET"])
def get_pdf(url):
    response = na_api.get_raw_na_url(url)
    pdf_content = response.content
    return Response(pdf_content, content_type='application/pdf')
