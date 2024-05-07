from flask import Flask
from app_factory import FlaskAppWrapper
from blueprints.atlas import atlas


flask_app = Flask(__name__)
app = FlaskAppWrapper(flask_app)
app.app.register_blueprint(atlas)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
