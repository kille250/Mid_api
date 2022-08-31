from flask import Blueprint, render_template
from db.user import User
from application import db


user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        return render_template("login/register.html")


@user_bp.route('/login')
def login():
    return render_template("login/login.html")
