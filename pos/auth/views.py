from flask import Blueprint, request, url_for, redirect
from flask_login import login_user, logout_user

from ..user import User

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.post("/login")
def login():
    user = User.query.get({'email': request.form["email"]})

    if user is None or user.password != request.form["password"]:
        return redirect(url_for("login"))
    login_user(user)
    return redirect(url_for("protected"))


@auth.post("/register")
def register():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        return redirect(url_for("register"))
   
    user = User(username, email, password)
    user.save()
    login_user(user)
    return redirect(url_for("protected"))


@auth.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
