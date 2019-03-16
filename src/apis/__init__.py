from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from apis import config

app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",title = "Something")

@app.route("/about")
def about():
    return "<h1>About Page</h1>"

# @app.route("/register")
# def register():
#     form = RegistrationForm()
#     return render_template('register.html',title = 'Register', form = form)
#
# @app.route("/login")
# def register():
#     form = LoginForm()
#     return render_template('login.html',title = 'Login', form = form)
db = MongoEngine(app)

from .auth import auth
from .judge import judge
from .auth import login_manager

app.register_blueprint(auth)
app.register_blueprint(judge, url_prefix='/judge')
login_manager.init_app(app)
