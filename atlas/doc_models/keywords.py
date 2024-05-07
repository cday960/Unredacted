from typing import Any


class Keywords:
    def __init__(
        self,
        text: str = "",
        relevance: float = 0.0,
        count: int = 0,
        raw_json: Any = None,
    ):

        if raw_json is not None:
            self.text = raw_json["text"]
            self.relevance = raw_json["relevance"]
            self.count = raw_json["count"]
        else:
            self.text = text
            self.relevance = relevance
            self.count = count

    def to_dict(self) -> dict:
        return {"text": self.text, "relevance": self.relevance, "count": self.count}
