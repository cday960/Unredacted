class DigitalObject:
    def __init__(
        self,
        filename: str,
        url: str,
        type: str,
        description: str,
        summary: str = None,
    ):
        self.filename = filename
        self.url = url
        self.type = type
        self.description = description
        self.summary = summary

    def to_dict(self):
        return {
            "filename": self.filename,
            "url": self.url,
            "type": self.type,
            "description": self.description,
            "summary": self.summary,
        }
