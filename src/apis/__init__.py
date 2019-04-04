from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from apis import config

app = Flask(__name__)
app.config.from_object(config)
db = MongoEngine(app)

# every thing that require db operation should be after this line

"""
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",title = "Something")

@app.route("/about")
def about():
    return "<h1>About Page</h1>"
"""
# here we create instance for bots of all platforms
from apis.bots import codeforces_bot
bot_list=\
    {
        "codeforces" : codeforces_bot(),
    }


from .auth import auth
from .judge import judge
from .auth import login_manager

app.register_blueprint(auth)
app.register_blueprint(judge, url_prefix='/judge')
login_manager.init_app(app)
