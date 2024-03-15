import os
import json
import requests

from flask import Blueprint, jsonify
from dotenv import load_dotenv
from models import Document

from util.search import na_id_search

webapp = Blueprint("webapp", __name__, url_prefix="/webapp")

load_dotenv()

api_url = "https://catalog.archives.gov/api/v2/"
api_key = str(os.getenv("API_KEY"))
headers = {"Content-Type": "application/json", "x-api-key": api_key}


@webapp.route("/search/<string:search_parameters>/<int:result_limit>", methods=["GET"])
@webapp.route("/search/<string:search_parameters>", methods=["GET"])
def webapp_search(search_parameters: str, result_limit: int = 20):
    """
    127.0.0.1:5000/webapp/search/<search_parameters>
    Example: 127.0.0.1:5000/webapp/search/john+f+kennedy
        + acts as a space in a url
    """
    doc_list = []

    url = (
        f"{api_url}records/search?q={search_parameters}&limit={result_limit}"
        "&levelOfDescription=item"
    )

    json_response = json.loads(requests.get(url, headers=headers).text)

    for result in json_response["body"]["hits"]["hits"]:
        print(json.dumps(result, indent=2))
        doc = Document(
            title=result["_source"]["record"]["title"],
            naId=result["_id"],
            uuid=result["_source"]["metadata"]["uuid"],
            filename=result["_source"]["metadata"]["fileName"],
            doc_type=result["_type"],
            date=result["_source"]["metadata"]["ingestTime"],
        )

        # Some records have no digitalObjects
        try:
            doc.digitalObjects = [
                {
                    "filename": obj.get("objectFilename"),
                    "url": obj.get("objectUrl"),
                    "type": obj.get("objectType"),
                    "description": obj.get("objectDescription"),
                }
                # limiting to five to make data a little easier to sift through
                for obj in result["_source"]["record"]["digitalObjects"][0:5]
            ]
        except KeyError:
            print(
                f"ERROR: the document has no digital objects"
                f"(naId: {doc.naId}, filetype: {doc.filename[-3:]})"
            )
            doc.digitalObjects = []

        doc_list.append(doc.to_dict())

    return jsonify({"data": doc_list})


@webapp.route("/record/id/<string:naId>", methods=["GET"])
@webapp.route("/record/id/<string:naId>?<string:uuid>", methods=["GET"])
def webapp_records(naId: str, uuid: str = ""):
    if naId is None:
        return jsonify({"error": "invalid naId parameters given"}), 400

    doc = na_id_search(naId)

    return jsonify({"data": doc.to_dict()})
