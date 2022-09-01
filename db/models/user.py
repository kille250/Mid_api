from database import db
from flask_login import UserMixin
from loginmanager import login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Invite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, unique=True)
    status = db.Column(db.Boolean, default=False)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
