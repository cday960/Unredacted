import os
import requests
import json

from flask import Flask, jsonify
from dotenv import load_dotenv

from app_factory import FlaskAppWrapper
from models import Document


load_dotenv()

api_url = "https://catalog.archives.gov/api/v2/"
api_key = str(os.getenv("API_KEY"))

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

    url = f"{api_url}records/search?q={search_parameters}&limit={result_limit}"

    headers = {"Content-Type": "application/json", "x-api-key": api_key}

    json_response = json.loads(requests.get(url, headers=headers).text)

    for result in json_response["body"]["hits"]["hits"]:
        # print(json.dumps(json_response, indent=2))

        title = result["_source"]["record"]["title"]
        id = result["_source"]["metadata"]["controlGroup"]["naId"]
        uuid = result["_source"]["metadata"]["uuid"]
        filename = result["_source"]["metadata"]["fileName"]
        doc_type = result["_type"]
        date = result["_source"]["metadata"]["ingestTime"]
        doc = Document(title, id, uuid, filename, doc_type, date)

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
                f"(uuid: {uuid}, filetype: {filename[-3:]})"
            )
            doc.digitalObjects = []

        doc_list.append(doc.to_dict())

    return jsonify({"data": doc_list})


# @app.route("/webapp/records/<string:uuid>", methods=["GET"])
# def webapp_search(uuid: str = ""):


if __name__ == "__main__":
    print(api_key)
    app.run(host="127.0.0.1", port=5000, debug=True)
