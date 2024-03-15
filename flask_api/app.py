import os

from flask import Flask
from dotenv import load_dotenv

from app_factory import FlaskAppWrapper
from models import Document

from blueprints.webapp import webapp
from blueprints.nlp import nlp

load_dotenv()

api_url = "https://catalog.archives.gov/api/v2/"
api_key = str(os.getenv("API_KEY"))
headers = {"Content-Type": "application/json", "x-api-key": api_key}

flask_app = Flask(__name__)
app = FlaskAppWrapper(flask_app)

app.app.register_blueprint(webapp)
app.app.register_blueprint(nlp)


if __name__ == "__main__":
    print(api_key)
    app.run(host="127.0.0.1", port=5000, debug=True)
