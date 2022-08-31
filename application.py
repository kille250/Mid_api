from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.api import api_bp
from post.post import post_bp
from user.user import user_bp


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    app.register_blueprint(user_bp, url_prefix="/")
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(post_bp, url_prefix='/generate')
    return app
