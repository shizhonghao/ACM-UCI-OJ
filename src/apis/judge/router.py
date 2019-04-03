from flask import Blueprint
from apis.models import User, OnlineJudge, Problem, Submission, Contest

judge = Blueprint('judge', __name__)

@judge.route('/contest')
def contest():
	return "list here"

@judge.route('/test')
def test():
	test_user = User(name='test',password='password', email='test@test.com')
	test_user.save()
	test_problem = Problem()
	oj = OnlineJudge(name='TestJudge')
	oj.save()
	return "problem here"

@judge.route('/submission')
def submission():
	return "show submission"

@judge.route('/submit')
def submit():
	return "submit"

@judge.route('/new_contest')
def new_contest():
	return "new contest"

