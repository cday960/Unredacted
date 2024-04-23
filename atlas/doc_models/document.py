import json
from typing import Any, Optional, Union, List, Dict
import datetime
from json import JSONEncoder
from .digital_object import DigitalObject
from .keywords import Keywords


# class Encoder(JSONEncoder):
#     def default(self, o):
#         if isinstance(o, Document):
#             return o.to_dict()
#         return JSONEncoder.default(self, o)


class Document:
    def __init__(
        self,
        title: str = "",
        naId: int = 0,
        uuid: str = "",
        # sort: Optional[Tuple[float, str]] = None,
        filename: str = "",
        doc_type: str = "",
        # date: datetime.datetime = datetime.datetime.now(),
        digitalObjects: Optional[List[DigitalObject]] = None,
        keywords: Optional[List[Keywords]] = None,
        raw_json: Any = None,
    ):

        if raw_json is not None:
            self.title = raw_json["title"]
            self.naId = raw_json["naId"]
            self.filename = raw_json["filename"]
            self.doc_type = raw_json["doc_type"]
            # self.date = raw_json["date"]
            self.digitalObjects = []
            self.keywords = []
            try:
                for obj in raw_json["digitalObjects"]:
                    self.digitalObjects.append(DigitalObject(raw_json=obj))
                for key in raw_json["keywords"]:
                    self.keywords.append(Keywords(raw_json=key))
            except KeyError:
                pass
        else:
            self.title = title
            self.naId = naId
            self.uuid = uuid
            # self.sort = sort
            self.filename = filename
            self.doc_type = doc_type
            # self.date = date
            self.digitalObjects = digitalObjects if digitalObjects is not None else []
            self.keywords = [] if keywords is None else keywords

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
    ) -> Dict[str, Union[str, int, Optional[List[Dict[str, str]]]]]:
        return {
            "title": self.title,
            "naId": self.naId,
            "filename": self.filename,
            "doc_type": self.doc_type,
            # "date": self.date,
            "digitalObjects": [obj.to_dict() for obj in self.digitalObjects],
            "keywords": [key.to_dict() for key in self.keywords],
        }
