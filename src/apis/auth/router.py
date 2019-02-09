from flask import Blueprint

auth = Blueprint('auth', __name__)
from flask_login import LoginManager

@auth.route("/")
def auth_home():
	return "home path"

@auth.route("/register")
def register():
	return "register here"

@auth.route("/login")
def login():
	return "login here"

@auth.route("/logout")
def logout():
	return "logout here"