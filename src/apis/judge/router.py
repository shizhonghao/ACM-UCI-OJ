from flask import Blueprint

judge = Blueprint('judge', __name__)

@judge.route('/contest_list')
def contest_list():
	return "list here"