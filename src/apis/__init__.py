from flask import Flask
from flask_mongoengine import MongoEngine
from .auth import auth
from .judge import judge

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(judge, url_prefix='/judge')

db = MongoEngine(app)