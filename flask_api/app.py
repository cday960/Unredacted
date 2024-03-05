import os
import requests
import json

from flask import Flask, jsonify, request
from dotenv import load_dotenv

from app_factory import FlaskAppWrapper
from models import Document


load_dotenv()

api_url = "https://catalog.archives.gov/api/v2/"
api_key = str(os.getenv("API_KEY"))

flask_app = Flask(__name__)
app = FlaskAppWrapper(flask_app)


def webapp_search(search_parameters: str):
    """
    127.0.0.1:5000/webapp/search/<search_parameters>
    Example: 127.0.0.1:5000/webapp/search/john+f+kennedy
        + acts as a space in a url
    """
    doc_list = []

    url = api_url + "records/search?q=" + search_parameters

    headers = {"Content-Type": "application/json", "x-api-key": api_key}

    json_response = json.loads(requests.get(url, headers=headers).text)

    for result in json_response["body"]["hits"]["hits"]:
        title = result["_source"]["record"]["title"]
        id = result["_id"]
        uuid = result["_source"]["metadata"]["uuid"]
        filename = result["_source"]["metadata"]["fileName"]
        doc_type = result["_type"]
        doc = Document(title, id, uuid, filename, doc_type)

        # Some records have no digitalObjects
        try:
            doc.digitalObjects = [
                {
                    "filename": obj.get("objectFilename"),
                    "url": obj.get("objectUrl"),
                    "type": obj.get("objectType"),
                }
                for obj in result["_source"]["record"]["digitalObjects"]
            ]
        except KeyError:
            print(f"ERROR: the document has no digital objects (uuid: {uuid})")
            doc.digitalObjects = []

        doc_list.append(doc.to_dict())

    return jsonify({"data": doc_list})


app.add_endpoint(
    "/webapp/search/<string:search_parameters>", "webapp_search", webapp_search
)


if __name__ == "__main__":
    print(api_key)
    app.run(host="127.0.0.1", port=5000, debug=True)
