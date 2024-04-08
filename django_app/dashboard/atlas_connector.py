import requests
import json
from .models import Document
import os
from dotenv import load_dotenv

load_dotenv()

ATLAS_URL = str(os.getenv("ATLAS_URL"))
print(f"Atlas URL: {ATLAS_URL}")

ATLAS_HEADERS = {"Content-Type": "application/json"}


def get_from_atlas(url: str, arg: str = None) -> requests.Response:
    atlas_response = None
    try:
        atlas_response = requests.get(
                url if arg is None else f"{url}/{arg}",
                headers=ATLAS_HEADERS,
            )
    except Exception as e:
        print(f"Error connecting to Atlas: {e}")
    return atlas_response
    

def get_recent_docs(num_docs: int = 5) -> list[Document]:
    atlas_response = get_from_atlas(f"{ATLAS_URL}/recent", num_docs).json()
    recent_docs = atlas_response['data']
    return recent_docs

def get_search_results(query: str) -> list[Document]:

    search_results = None

    if query[-1] == '+':
        query = query[:-1]
    valid_query = False
    for char in query:
        if char != '+':
            valid_query = True

    if valid_query:
        search_results = json.loads(get_from_atlas(f"{ATLAS_URL}/search", arg = query).text)['data']

    return search_results


def get_document(naId: int) -> Document:
    doc = Document(raw_json=get_from_atlas(f"{ATLAS_URL}/record", arg = naId).json()['data'])
    return doc


def get_pdf(url: str) -> bytes:
    return get_from_atlas(f"{ATLAS_URL}/pdf", arg = url).content

