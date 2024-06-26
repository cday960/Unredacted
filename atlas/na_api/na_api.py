import json
import requests
from doc_models import Document, DigitalObject
from .na_utils import (
    swap_spaces_for_plus,
    valid_date_param,
    get_docs_from_na_json_response,
)
from .na_env import HEADERS, NA_API_URL


def get_doc_from_na(naId: int) -> Document:
    try:
        url = f"{NA_API_URL}/records/search?naId={naId}"
        json_response = json.loads(requests.get(url, headers=HEADERS).text)
        if json_response is not None:
            doc = get_docs_from_na_json_response(json_response)[0]
            return doc
        else:
            raise Exception
    except Exception as e:
        raise RuntimeError(f"Error in doc retrieval with naId = {naId}: {e}")


def get_raw_na_url(url: str) -> requests.Response:
    return requests.get(url, headers=HEADERS)


def query_pdf_documents(
    q: str = "*",
    limit: int = 200,
    page: int = -1,
    start_date: str = None,
    end_date: str = None,
    personOrOrg: str = None,
    title: str = None,
) -> list[Document]:

    try:
        # construct URL
        url = f"{NA_API_URL}/records/search?q={q}&objectType=PDF&limit={limit}&levelOfDescription=item"
        if page >= 0:
            url += f"&page={page}"
        if start_date is not None and valid_date_param(start_date):
            url += f"&startDate={start_date}"
        if end_date is not None and valid_date_param(end_date):
            url += f"&endDate={end_date}"
        if personOrOrg is not None:
            personOrOrg = swap_spaces_for_plus(personOrOrg)
            url += f"&personOrOrg={personOrOrg}"
        if title is not None:
            title = swap_spaces_for_plus(title)
            url += f"&title={title}"

        # run URL through NA API
        json_response = json.loads(requests.get(url, headers=HEADERS).text)

        doc_list = get_docs_from_na_json_response(json_response)

        return doc_list

    except Exception as e:
        raise RuntimeError(f"Error in PDF query with query = {q}: {e}")
