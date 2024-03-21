from typing import Any
from models import Document, DigitalObject

def fill_doc_from_db_json(db_json: dict[str, Any]) -> Document:
        doc: Document = None
        if db_json is not None:
            doc = Document(
                title=db_json["title"],
                naId=db_json["naId"],
                filename=db_json["filename"],
                doc_type=db_json["doc_type"],
                date=db_json["date"],
                digitalObjects=[
                    DigitalObject(
                        filename=obj["filename"],
                        url=obj["url"],
                        type=obj["type"],
                        description=obj["description"],
                        summary=obj["summary"],
                    )
                    for obj in db_json["digitalObjects"]
                ],
            )
        return doc