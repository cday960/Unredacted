import os
import json
import requests
from dotenv import load_dotenv

from models import Document, DigitalObject
from .na_utils import swap_spaces_for_plus, valid_date_param

load_dotenv()

API_KEY = str(os.getenv("API_KEY"))
print(f"National Archives Key: {API_KEY}")


API_URL = "https://catalog.archives.gov/api/v2/"
HEADERS = {"Content-Type": "application/json", "x-api-key": API_KEY}


def na_id_search(naId: str) -> Document:
    url = f"{API_URL}records/search?objectType=PDF?naId={naId}"

    json_response = json.loads(requests.get(url, headers=HEADERS).text)
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


def get_pdf_documents(q: str = "*", 
                      limit: int = 200, 
                      page: int = -1,
                      start_date: str = None, 
                      end_date: str = None, 
                      personOrOrg: str = None,
                      title: str = None,) -> list[Document]:
    
    doc_list = []
    
    # construct URL
    url = f"{API_URL}/records/search?objectType=PDF?limit={limit}?q={q}"
    if page >= 0:
        url += f"?page={page}"
    if start_date is not None and valid_date_param(start_date):
        url += f"?startDate={start_date}"
    if end_date is not None and valid_date_param(end_date):
        url += f"?endDate={end_date}"
    if personOrOrg is not None: 
        personOrOrg = swap_spaces_for_plus(personOrOrg)
        url += f"?personOrOrg={personOrOrg}"
    if title is not None:
        title = swap_spaces_for_plus(title)
        url += f"?title={title}"

    # run URL through NA API
    json_response = json.loads(requests.get(url, headers=HEADERS).text)

    # load the doc list from json
    for json_doc in json_response["body"]["hits"]["hits"]:
        doc = Document(
            title=json_doc["_source"]["record"]["title"],
            naId=json_doc["_id"],
            uuid=json_doc["_source"]["metadata"]["uuid"],
            filename=json_doc["_source"]["metadata"]["fileName"],
            doc_type=json_doc["_type"],
            date=json_doc["_source"]["metadata"]["ingestTime"],
        )

        try:
            for do in json_response["_source"]["record"]["digitalObjects"]:
                doc.digitalObjects.append(DigitalObject(
                    filename = do.get("objectFilename"),
                    url = do.get("objectUrl"),
                    type = do.get("objectType"),
                    description = do.get("objectDescription"),
                    
                ))
            doc_list.append(doc)
        except KeyError:
            print(
                f"ERROR: the document has no digital objects"
                f"(naId: {doc.naId}, filetype: {doc.filename[-3:]})"
            )

    return doc_list

    

    
    
