from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

api_url = "https://catalog.archives.gov/api/v2/"
api_key = ""


@app.route("/")
def home():
    return "Welcome to the Unredacted API!"


@app.route("/webapp/search", methods=["POST"])
def webapp_search():
    request_str = str(request.data)
    request_json = request.get_json()

    parameters = request_json["search_parameters"]
    url = api_url + "records/search?q=" + parameters[0]

    headers = {"Content-Type": "application/json", "x-api-key": api_key}

    na_api_response = requests.get(api_url, headers=headers)
    print(na_api_response.text)
    return "uhh"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
