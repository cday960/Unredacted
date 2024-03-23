import os
from dotenv import load_dotenv

load_dotenv()

NA_API_URL = "https://catalog.archives.gov/api/v2"
NA_API_KEY = str(os.getenv("NA_API_KEY"))
HEADERS = {"Content-Type": "application/json", "x-api-key": NA_API_KEY}

print(f"National Archives API Key: {NA_API_KEY}")
