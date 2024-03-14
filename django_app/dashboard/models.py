# Create your models here.
import json
from typing import Dict, List, Optional, Any, Union
import datetime
from json import JSONEncoder


class Encoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)
    
class PageContext:
    def __init__(self, test: str = "Test Value", title: str = "Title", data: Any = None):
        self.test = test
        self.title = title
        self.data = data

    def to_dict(self) -> dict[str, Any]:
        return {"test": self.test, "title": self.title, "data": self.data}

class PageInfo:
    def __init__(self, render: str, context: PageContext):
        self.render = render
        self.context = context
        self.previous_render = render
        self.previous_context = context

    def get_render(self) -> str:
        return self.render

    def get_context(self) -> PageContext:
        return self.context
    
    def get_render_context(self) -> tuple[str, PageContext]:
        return (self.render, self.context)
    
    def get_render_context_dict(self) -> tuple[str, dict[str, Any]]:
        return (self.render, self.context.to_dict())

    def set_render(self, render: str) -> None:
        self.previous_render = self.render
        self.render = render

    def set_context(self, context: PageContext) -> None:
        self.previous_context = self.context
        self.context = context

    def set_render_context(self, render: str, context: PageContext) -> None:
        self.set_render(render)
        self.set_context(context)

    def revert(self) -> None:
        self.set_render(self.previous_render)
        self.set_context(self.previous_context)



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
    ) -> Dict[str, Union[str, int, datetime.datetime, Optional[List[Dict[str, str]]]]]:
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
