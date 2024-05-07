# Create your models here.

from typing import Any
from typing import Any, Optional, Union, List, Dict
import datetime


class DigitalObject:
    def __init__(
        self,
        filename: str = "",
        url: str = "",
        file_type: str = "",
        description: str = "No descripition was provided.",
        summary: str = "Summary still processing. Please check back later!",
        raw_json: Any = None,
    ):
        if raw_json is not None:
            self.filename = raw_json["filename"]
            self.url = raw_json["url"]
            self.file_type = raw_json["file_type"]
            self.description = raw_json["description"]
            self.summary = raw_json["summary"]
        else:
            self.filename = filename
            self.url = url
            self.file_type = file_type
            self.description = description
            self.summary = summary

    def to_dict(self):
        return {
            "filename": self.filename,
            "url": self.url,
            "file_type": self.file_type,
            "description": self.description,
            "summary": self.summary,
        }


class Document:
    def __init__(
        self,
        title: str = "",
        naId: int = 0,
        uuid: str = "",
        # sort: Optional[Tuple[float, str]] = None,
        filename: str = "",
        doc_type: str = "",
        date: datetime.datetime = datetime.datetime.now(),
        digitalObjects: Optional[List[DigitalObject]] = None,
        raw_json: Any = None,
    ):
        if raw_json is not None:
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
    ) -> Dict[str, Union[str, int, Optional[List[Dict[str, str]]]]]:
        return {
            "title": self.title,
            "naId": self.naId,
            "filename": self.filename,
            "doc_type": self.doc_type,
            "date": self.date,
            "digitalObjects": [obj.to_dict() for obj in self.digitalObjects],
        }


class ApiEndpoint:
    def __init__(self, endpoint: str, info: str):
        self.endpoint = endpoint
        self.info = info

    def to_dict(self) -> Dict[str, str]:
        return {"endpoint": self.endpoint, "info": self.info}
