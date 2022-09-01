from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_database(app):
    db.init_app(app)
    #db.create_all(app=app)
    return db
