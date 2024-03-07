import json
from typing import Dict, List, Optional, Any
import datetime
from json import JSONEncoder


class Encoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)


class Document:
    def __init__(
        self,
        title: str = "",
        naId: int = 0,
        filename: str = "",
        doc_type: str = "",
        date: datetime.datetime = datetime.datetime.now(),
        digitalObjects: Optional[List[Dict[str, str]]] = None,
    ):
        self.title = title
        self.naId = naId
        self.filename = filename
        self.doc_type = doc_type
        self.date = date
        self.digitalObjects = digitalObjects if digitalObjects is not None else []

    # debugging func to see info ab document
    def __repr__(self) -> str:
        return f"doc {self.title}: {self.naId}"

    # printing function, this function overloads print(<Document>)
    def __str__(self) -> str:
        return (
            f"{self.title}\n\tID: {self.naId}\n\t"
            f"Filename: {self.filename}\n\tDoc type: {self.doc_type}\n\t"
            f"Number of objects: {len(self.digitalObjects)}"
        )

    # converts obj to dict
    def to_dict(
        self,
    ) -> Dict[str, str | int | datetime.datetime | Optional[List[Dict[str, str]]]]:
        return {
            "title": self.title,
            "naId": self.naId,
            "filename": self.filename,
            "doc_type": self.doc_type,
            "date": self.date,
            "digitalObjects": self.digitalObjects,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), cls=Encoder)
