from flask import Blueprint
from flask_login import LoginManager

from apis.models import User

auth = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
	return User.get(user_id)

# --- below are the routes used for authentication

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
    logout_user()
    return redirect(somewhere)