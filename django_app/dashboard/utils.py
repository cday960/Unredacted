import os
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import requests
from doc_models import Document, DigitalObject

load_dotenv()

MONGO_URI = str(os.getenv("MONGO_URI"))
DB_NAME = "UnredactedDB1"
COLLECTION_NAME = "DocumentData"

# Initial connection
client = MongoClient(MONGO_URI, server_api=ServerApi("1"))

# Send a ping to confirm a successful connection
client.admin.command("ping")
print("Pinged deployment. Successfully connected to MongoDB.")

# Access the database
db = client[DB_NAME]

# Access the collection
collection = db[COLLECTION_NAME]


def get_recent_docs(num_docs: int = 10) -> list[Document]:
    recent_docs = []
    results = collection.find().sort("_id", -1).limit(num_docs)
    for result in results:
        recent_docs.append(Document(raw_json=result))
    return recent_docs


""" 
Quick NA connector
"""
NA_API_URL = "https://catalog.archives.gov/api/v2"
NA_API_KEY = str(os.getenv("NA_API_KEY"))
NA_HEADERS = {"Content-Type": "application/json", "x-api-key": NA_API_KEY}

print(f"National Archives API Key: {NA_API_KEY}")


def get_raw_na_url(url: str) -> requests.Response:
    return requests.get(url, headers=NA_HEADERS)
