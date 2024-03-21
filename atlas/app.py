from flask import Flask
from app_factory import FlaskAppWrapper
from blueprints.webapp import webapp


flask_app = Flask(__name__)
app = FlaskAppWrapper(flask_app)
app.app.register_blueprint(webapp)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
