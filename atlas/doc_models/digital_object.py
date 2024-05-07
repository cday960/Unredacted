from typing import Any


class DigitalObject:
    def __init__(
        self,
        filename: str,
        url: str,
        file_type: str,
        description: str = "No description is provided for the document",
        summary: str = "Summary still processing. Please check back later!",
        raw_json: Any = None,
    ):
        if raw_json is not None:
            self.filename = raw_json["filename"]
            self.url = raw_json["url"]
            self.file_type = raw_json["file_type"]
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
            "file_type": self.file_type,
            "description": self.description,
            "summary": self.summary,
        }
