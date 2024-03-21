
from flask import Blueprint, jsonify
from models import Document
from utils import search_logic


webapp = Blueprint("webapp", __name__, url_prefix="/webapp")


@webapp.route("/search/<string:search_parameters>/<int:result_limit>", methods=["GET"])
@webapp.route("/search/<string:search_parameters>", methods=["GET"])
def webapp_search(search_parameters: str, result_limit: int = 20):
    """
    127.0.0.1:5000/webapp/search/<search_parameters>
    Example: 127.0.0.1:5000/webapp/search/john+f+kennedy
        + acts as a space in a url
    """

    if search_parameters is None:
        return jsonify({"error": "invalid search parameters given"}), 400

    doc_list: list[Document] = search_logic.get_search_results(search_parameters)

    return jsonify({"data": doc_list})


@webapp.route("/record/id/<string:naId>", methods=["GET"])
@webapp.route("/record/id/<string:naId>?<string:uuid>", methods=["GET"])
def webapp_records(naId: str, uuid: str = ""):
    if naId is None:
        return jsonify({"error": "invalid naId parameters given"}), 400
    
    doc = search_logic.get_doc(naId)

    return jsonify({"data": doc.to_dict()})
