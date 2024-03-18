from typing import Any


class DigitalObject:
    def __init__(
        self,
        filename: str = "",
        url: str = "",
        file_type: str = "",
        description: str = "",
        summary: str = "",
        raw_json: Any = None,
    ):
        if raw_json is not None:
            self.filename = raw_json["filename"]
            self.url = raw_json["url"]
            self.file_type = raw_json["type"]
            try:
                self.description = raw_json.get("description")
            except KeyError:
                self.description = ""
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
            "type": self.file_type,
            "description": self.description,
            "summary": self.summary,
        }
