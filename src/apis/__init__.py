from flask import Flask
from flask_mongoengine import MongoEngine
from apis import config

app = Flask(__name__)
app.config.from_object(config)

db = MongoEngine(app)

from .auth import auth
from .judge import judge
from .auth import login_manager

app.register_blueprint(auth)
app.register_blueprint(judge, url_prefix='/judge')
login_manager.init_app(app)
