from flask import Flask
from api.api import api_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    app.register_blueprint(api_bp, url_prefix='/api')
    return app
