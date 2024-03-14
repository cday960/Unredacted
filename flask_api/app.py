import os
from typing import Tuple
import requests
import json

from flask import Flask, jsonify
from dotenv import load_dotenv

from app_factory import FlaskAppWrapper
from models import Document


load_dotenv()

api_url = "https://catalog.archives.gov/api/v2/"
api_key = str(os.getenv("API_KEY"))
headers = {"Content-Type": "application/json", "x-api-key": api_key}

flask_app = Flask(__name__)
app = FlaskAppWrapper(flask_app)


@app.route(
    "/webapp/search/<string:search_parameters>/<int:result_limit>", methods=["GET"]
)
@app.route("/webapp/search/<string:search_parameters>", methods=["GET"])
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

    """ ---------- Debugging ---------- """
    # uh = requests.get(url, headers=headers).json()["body"]["hits"]["hits"]
    # print(json.dumps(uh, indent=2))

    """ ---------- Debugging ---------- """

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

    """ ---------- Debugging ---------- """
    # print("Doc List")
    # print(json.dumps(doc_list, indent=2))

    """ ---------- Debugging ---------- """

    return jsonify({"data": doc_list})


@app.route("/webapp/records/id/<string:naId>", methods=["GET"])
@app.route("/webapp/records/id/<string:naId>?<string:uuid>", methods=["GET"])
def webapp_records(naId: str, uuid: str = ""):
    if naId is None:
        return jsonify({"error": "invalid naId parameters given"}), 400

    url = f"{api_url}records/search?naId={naId}"

    json_response = json.loads(requests.get(url, headers=headers).text)
    json_response = json_response["body"]["hits"]["hits"][0]

    """ ---------- Debugging ---------- """
    # temp_response = json_response["body"]["hits"]["hits"]
    # temp = {}
    # for x in temp_response:
    #     temp[x["_source"]["record"]["title"]] = {
    #         "id": x["_id"],
    #         "metadata": x["_source"]["metadata"],
    #     }

    # temp = {
    #     x["_source"]["record"]["title"]: x["_source"]["metadata"] for x in temp_response
    # }

    # temp["number of hits"] = len(temp_response)
    # print(json.dumps(temp, indent=2))

    """ ---------- Debugging ---------- """

    doc = Document(
        title=json_response["_source"]["record"]["title"],
        naId=json_response["_id"],
        uuid=json_response["_source"]["metadata"]["uuid"],
        filename=json_response["_source"]["metadata"]["fileName"],
        doc_type=json_response["_type"],
        date=json_response["_source"]["metadata"]["ingestTime"],
    )

    try:
        for x in json_response["_source"]["record"]["digitalObjects"]:
            print(x)
            doc.digitalObjects.append(
                {
                    "filename": x.get("objectFilename"),
                    "url": x.get("objectUrl"),
                    "type": x.get("objectType"),
                    "description": x.get("objectDescription"),
                }
            )
    except KeyError:
        print(
            f"ERROR: the document has no digital objects"
            f"(naId: {doc.naId}, filetype: {doc.filename[-3:]})"
        )

    """ ---------- Debugging ---------- """
    # print(doc.to_json())

    """ ---------- Debugging ---------- """

    return jsonify({"data": doc.to_dict()})


if __name__ == "__main__":
    print(api_key)
    app.run(host="127.0.0.1", port=5000, debug=True)
