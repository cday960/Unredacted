import json
from typing import Dict, List, Optional, Any, Union
import datetime
from json import JSONEncoder


class Encoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return JSONEncoder.default(self, o)


class Document:
    def __init__(
        self,
        title: str = "",
        naId: Tuple[int, int] = (0, 0),
        uuid: str = "",
        # sort: Optional[Tuple[float, str]] = None,
        filename: str = "",
        doc_type: str = "",
        date: datetime.datetime = datetime.datetime.now(),
        digitalObjects: Optional[List[Dict[str, str]]] = None,
    ):
        self.title = title
        self.naId = naId
        self.uuid = uuid
        # self.sort = sort
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
            "digitalObjects": self.digitalObjects,
        }
        return ret

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), cls=Encoder)
