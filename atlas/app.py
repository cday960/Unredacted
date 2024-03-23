from flask import Flask
from app_factory import FlaskAppWrapper
from blueprints.atlas import atlas
from nlp_utils import start_doc_processing


flask_app = Flask(__name__)
app = FlaskAppWrapper(flask_app)
app.app.register_blueprint(atlas)

if __name__ == "__main__":
    start_doc_processing()
    app.run(host="127.0.0.1", port=5000, debug=True)
