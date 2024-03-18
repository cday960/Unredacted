from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from doc_models import Document
from typing import Any
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = str(os.getenv("MONGO_URI"))

# Connect to MongoDB
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Access the database
db = client['UAPI-Data']

# Access the collection
collection = db['DocumentData']

def db_get_doc(naId: int) -> Document:
    query = {"naId": naId}
    result = collection.find_one(query)
    print(result)
    return None

def db_doc_exists(doc: Document) -> bool:
    if collection.find_one(doc.to_dict()) is not None:
        return True
    else:
        return False


def db_insert_doc(doc: Document) -> bool:
    if collection.insert_one(doc.to_dict()) is not None:
        return True
    else:
        return False

