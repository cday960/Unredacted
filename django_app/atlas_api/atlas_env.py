import os
from dotenv import load_dotenv

load_dotenv()

ATLAS_API_URL = ""
ATLAS_API_KEY = str(os.getenv("ATLAS_API_KEY"))
HEADERS = {"Content-Type": "application/json", "x-api-key": ATLAS_API_KEY}

print(f"ATLAS API Key: {ATLAS_API_KEY}")