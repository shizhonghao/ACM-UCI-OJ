from flask_mongoengine import MongoEngine
from flask_login import UserMixin
from apis import db
from mongoengine import *


# user model
class User(UserMixin, db.Document):
    name = db.StringField(max_length=32, required=True, unique=True)
    password = db.StringField(max_length=255, required=True)
    email = db.StringField(max_length=255)
    is_admin = db.BooleanField(default=False)
    submission_list = db.ListField(db.ReferenceField('Submission'))


class OnlineJudge(db.Document):
    name = db.StringField(required=True, unique=True)
    #oj_id = db.IntField(required=True, unique=True)


class Problem(db.Document):
    online_judge = db.ReferenceField('OnlineJudge')
    problem_id = db.StringField(required=True)
    title = db.StringField(required=True)
    time_limit = db.StringField()
    memory_limit = db.StringField()
    description = db.StringField()
    input_format = db.StringField()
    output_format = db.StringField()
    sample_input = db.ListField(db.StringField())
    sample_output = db.ListField(db.StringField())


class Submission(db.Document):
    user = db.ReferenceField('User')
    problem = db.ReferenceField('Problem')
    submission_time = db.DateTimeField()
    submission_status = db.StringField()
    language = db.StringField()
    solution = db.StringField()


class Contest(db.Document):
    contest_name = db.StringField()
    organizer = db.ReferenceField('User')
    problem_list = db.ListField(db.ReferenceField('Problem'))
    participant_list = db.ListField(db.ReferenceField('User'))
    submission_list = db.ListField(db.ReferenceField('Submission'))
    start_time = db.DateTimeField()
    end_time = db.DateTimeField()

