import os
from dotenv import load_dotenv

load_dotenv()

NLP_API_KEY = str(os.getenv("NLP_API_KEY"))
NLP_API_URL = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/1645185e-ee50-492f-b1f3-5093f5094d51"

print(f"Watson API Key: {NLP_API_KEY}")