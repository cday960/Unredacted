from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from doc_models import Document, DigitalObject
from typing import Any
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = str(os.getenv("MONGO_URI"))



class MongoDb:

    def __init__(self):

        self.client = MongoClient(MONGO_URI, server_api=ServerApi("1"))

        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command("ping")
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        # Access the database
        self.db = self.client["UnredactedDB1"]

        # Access the collection
        self.collection = self.db["DocumentData"]


    @classmethod
    def fill_doc_from_json(cls, db_json: dict[str, Any]) -> Document:
        doc: Document = None
        if db_json is not None:
            doc = Document(
                title=db_json["title"],
                naId=db_json["naId"],
                filename=db_json["filename"],
                doc_type=db_json["doc_type"],
                date=db_json["date"],
                digitalObjects=[
                    DigitalObject(
                        filename=obj["filename"],
                        url=obj["url"],
                        type=obj["type"],
                        description=obj["description"],
                        summary=obj["summary"],
                    )
                    for obj in db_json["digitalObjects"]
                ],
            )
        return doc


    def get_doc(self, naId: int) -> Document:
        query = {"naId": str(naId)}
        result = self.collection.find_one(query)
        doc: Document = MongoDb.fill_doc_from_json(result)
        return doc


    def get_recent_docs(self, num_docs: int = 10) -> list[Document]:
        recent_docs = []
        results = self.collection.find().sort('_id', -1).limit(num_docs)
        for result in results:
            recent_docs.append(MongoDb.fill_doc_from_json(result))
        return recent_docs


    def doc_exists(self, doc: Document) -> bool:
        if self.collection.find_one(doc.to_dict()) is not None:
            return True
        else:
            return False


    def naId_exists(self, naId: int) -> bool:
        query = {"naId": str(naId)}
        result = self.collection.find_one(query)
        if result is not None:
            return True
        else:
            return False


    def insert_doc(self, doc: Document) -> bool:
        if self.collection.insert_one(doc.to_dict()) is not None:
            return True
        else:
            return False
