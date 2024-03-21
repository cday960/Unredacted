import re
from models import Document, DigitalObject

def valid_date_param(date: str) -> bool:
    date_pattern = "^\d{4}-\d{2}-\d{2}$"
    if re.match(date_pattern, date):
        return True
    else:
        return False

def swap_spaces_for_plus(params: str) -> str:
    params.replace(' ', '+')
    if params[len(params) - 1] == '+':
        params = params[:-1]
    return params


def get_docs_from_na_json_response(
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