from flask import Blueprint, render_template, flash, redirect,url_for
from flask_login import LoginManager
from apis.forms import RegistrationForm, LoginForm
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


@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@auth.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm() 
    return render_template('login.html', title='Login', form=form)


@auth.route("/logout")
def logout():
    # logout_user()
    return "logout"  # redirect(somewhere)
