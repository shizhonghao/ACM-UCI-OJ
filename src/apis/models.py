from flask_mongoengine import MongoEngine
from flask_login import UserMixin
from . import db

# user model
class User(UserMixin, db.Document):
    username = db.StringField(max_length=32, required=True, unique=True)
    password = db.StringField(max_length=255, required=True)
    email = db.StringField(max_length=255)
    is_admin = db.BooleanField(default=False)
