import os
import json
import requests
from dotenv import load_dotenv
from doc_models import Document, DigitalObject

load_dotenv()

NA_API_URL = "https://catalog.archives.gov/api/v2/"
NA_API_KEY = str(os.getenv("NA_API_KEY"))
HEADERS = {"Content-Type": "application/json", "x-api-key": NA_API_KEY}

print(f"National Archives API Key: {NA_API_KEY}")


def get_doc_list_from_na(search_parameters: str, result_limit: int = 20) -> list[Document]:
    url = (
        f"{NA_API_URL}records/search?q={search_parameters}&limit={result_limit}"
        "&levelOfDescription=item"
    )
    json_response = json.loads(requests.get(url, headers=HEADERS).text)
    doc_list = get_docs_from_json_response(json_response)
    return doc_list


def get_doc_from_na(naId: int) -> Document:
    url = f"{NA_API_URL}records/search?naId={naId}"
    json_response = json.loads(requests.get(url, headers=HEADERS).text)
    doc = get_docs_from_json_response(json_response)[0]
    return doc

def get_raw_na_url(url: str) -> requests.Response:
    return requests.get(url, headers=HEADERS)

def get_pdf_from_na(url: str):
    pdf = get_raw_na_url(url).content
    return pdf  



def get_docs_from_json_response(
    json_response: str, obj_limit: int = 20
) -> list[Document]:
    doc_list = []
    for result in json_response["body"]["hits"]["hits"]:
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
            # Some records have no digitalObjects, dont save them
            for obj in result["_source"]["record"]["digitalObjects"][0:obj_limit]:
                # only save files with only pdfs...for now
                if "PDF" in obj.get("objectType"):
                    doc.digitalObjects.append(
                        DigitalObject(
                            filename=obj.get("objectFilename"),
                            url=obj.get("objectUrl"),
                            type=obj.get("objectType"),
                            description=obj.get("objectDescription"),
                            # summary would be none
                        )
                    )
                else:
                    raise KeyError
            doc_list.append(doc)
        except KeyError:
            print(
                f"ERROR: the document has either no digital objects or non-pdf digital objects"
                f"(naId: {doc.naId}, filetype: {doc.filename[-3:]})"
            )
    return doc_list
