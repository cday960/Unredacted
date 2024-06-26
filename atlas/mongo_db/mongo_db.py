from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from doc_models import Document, DigitalObject
from typing import Any

from .db_env import MONGO_URI, DB_NAME, COLLECTION_NAME
from .db_utils import fill_doc_from_db_json

# Initial connection
client = MongoClient(MONGO_URI, server_api=ServerApi("1"))

# Send a ping to confirm a successful connection
client.admin.command("ping")
print("Pinged deployment. Successfully connected to MongoDB.")

# Access the database
db = client[DB_NAME]

# Access the collection
collection = db[COLLECTION_NAME]

collection.create_index([("title", "text"), ("keywords.text", "text")])


def query_db(query: dict[str, Any], limit=20) -> list[Document]:
    doc_list = []
    results = collection.find(query).limit(limit)
    for result in results:
        doc_list.append(fill_doc_from_db_json(result))
    return doc_list


def get_doc(naId: int) -> Document:
    query = {"naId": str(naId)}
    result = collection.find_one(query)
    doc: Document = fill_doc_from_db_json(result)
    return doc


def get_recent_docs(num_docs: int = 10) -> list[Document]:
    recent_docs = []
    results = collection.find().sort("_id", -1).limit(num_docs)
    for result in results:
        recent_docs.append(fill_doc_from_db_json(result))
    return recent_docs


def doc_exists(doc: Document) -> bool:
    if collection.find_one(doc.to_dict()) is not None:
        return True
    else:
        return False


def naId_exists(naId: int) -> bool:
    query = {"naId": str(naId)}
    result = collection.find_one(query)
    if result is not None:
        return True
    else:
        return False


def insert_doc(doc: Document) -> bool:
    if not collection.find_one({'naid': doc.naId}) and collection.insert_one(doc.to_dict()) is not None:
        return True
    else:
        return False


def keyword_search(
    keywords: list[str], start_date: int = None, end_date: int = None
) -> list[Document]:
    keyword_results: list[Document] = []
    pipeline = [
        {"$match": {"keywords.text": {"$in": keywords}}},
        {"$group": {"_id": "$_id", "relevance_score": {"$sum": "$keywords.count"}}},
        {"$sort": {"relevance_score": -1}},
    ]
    results = collection.aggregate(pipeline)
    for result in results:
        keyword_results.append(fill_doc_from_db_json(result))

    # for keyword in keywords:
    #     title_docs = collection.find({'$text': {'$search': keyword}})
    #     for result in title_docs:
    #         keyword_results.append(fill_doc_from_db_json(result))

    return keyword_results
