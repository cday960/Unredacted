import os
import json
import requests

from dotenv import load_dotenv
from models import Document

load_dotenv()

api_url = "https://catalog.archives.gov/api/v2/"
api_key = str(os.getenv("API_KEY"))
headers = {"Content-Type": "application/json", "x-api-key": api_key}


def na_id_search(naId: str) -> Document:
    url = f"{api_url}records/search?naId={naId}"

    json_response = json.loads(requests.get(url, headers=headers).text)
    json_response = json_response["body"]["hits"]["hits"][0]

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

    return doc
