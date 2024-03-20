# Create your models here.
from typing import Any
import datetime
from json import JSONEncoder


class Encoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)


class PageContext:
    def __init__(
        self, test: str = "Test Value", title: str = "Title", data: Any = None
    ):
        self.test = test
        self.title = title
        self.data = data

    def to_dict(self) -> dict[str, Any]:
        return {"test": self.test, "title": self.title, "data": self.data}


class PageInfo:
    def __init__(self, render: str, context: PageContext, avoid_switch: dict[str, str] = None):
        self.render = render
        self.context = context
        self.previous_render = render
        self.previous_context = context
        self.avoid_switch: dict[str, str] = avoid_switch if avoid_switch is not None else {}

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
        if self.previous_render in self.avoid_switch:
            self.previous_render = self.avoid_switch[self.previous_render]
        self.set_render(self.previous_render)
        self.set_context(self.previous_context)
