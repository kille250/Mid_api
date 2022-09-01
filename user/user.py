from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from db.models.user import User
from database import db


user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/register', methods=['GET'])
def register():
    return render_template("login/register.html")


@user_bp.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('lname')
    password = request.form.get('lpassword')

    user = User.query.filter_by(name=name).first()

    if user:
        flash('Username address already exists')
        return redirect(url_for("user_bp.register"))

    new_user = User(name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("user_bp.login"))


@user_bp.route('/login', methods=['GET'])
def login():
    return render_template("login/login.html")


@user_bp.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('lname')
    password = request.form.get('lpassword')

    user = User.query.filter_by(name=name).first()

    if not user or not check_password_hash(user.password, password):
        flash("Invalid Creditals")
        return redirect(url_for('user_bp.login'))

    login_user(user)
    return redirect('generate')


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_bp.login'))
