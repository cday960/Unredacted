import json
from typing import Any, Dict, List, Optional, Union
import datetime
from json import JSONEncoder
from .digital_object import DigitalObject


class Encoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return JSONEncoder.default(self, o)


class Document:
    def __init__(
        self,
        title: str = "",
        naId: int = 0,
        filename: str = "",
        doc_type: str = "",
        date: datetime.datetime = datetime.datetime.now(),
        digitalObjects: Optional[List[DigitalObject]] = [],
        raw_json: Any = None,
    ):
        if raw_json is not None:
            print(raw_json)
            self.title = raw_json["title"]
            self.naId = raw_json["naId"]
            self.filename = raw_json["filename"]
            self.doc_type = raw_json["doc_type"]
            self.date = raw_json["date"]
            self.digitalObjects = []
            for obj in raw_json["digitalObjects"]:
                self.digitalObjects.append(DigitalObject(raw_json=obj))
        else:
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
    ) -> Dict[str, Union[str, int, datetime.datetime, Optional[List[Dict[str, str]]]]]:
        return {
            "title": self.title,
            "naId": self.naId,
            "filename": self.filename,
            "doc_type": self.doc_type,
            "date": self.date,
            "digitalObjects": [obj.to_dict() for obj in self.digitalObjects],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), cls=Encoder)
