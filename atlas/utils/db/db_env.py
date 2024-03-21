import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = str(os.getenv("MONGO_URI"))
DB_NAME = "UnredactedDB1"
COLLECTION_NAME = "DocumentData"
