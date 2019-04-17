from flask import request, jsonify, Blueprint
from apis.models import User, OnlineJudge, Problem, Submission, Contest
from apis import bot_list

judge = Blueprint('judge', __name__)

@judge.route('/contest_list')
def contest_list():
    return "list here"

@judge.route('/test')
def test():
    #test_user = User(name='test',password='password', email='test@test.com')
    #test_user.save()
    test_problem = Problem()
    oj = OnlineJudge(name='codeforces')
    oj.save()
    return "problem here"

# Content-Type: application/json;
# body:{"oj", "contest", "problem_id", "language", "code" }
@judge.route('/submit')
def submit():
    data = request.get_json()
    print("New submission on:", data["oj"], data["contest"], data["problem_id"], data["language"])
    # !!!to be implemented!!!
    # add submission to database
    #submission = Submission.objects(problem=)
    #if not :
    if data["oj"] not in bot_list:
        print("oj in query not found.")
        return jsonify({"success" : "false", "message" : "Invalid OJ name"})
    bot = bot_list[data["oj"]]
    status_code = bot.submit(data["contest"], data["problem_id"], data["language"], data["code"])
    if status_code > 400:
        # !!!to be implemented!!!
        # change submission status on the database to false
        return jsonify({"success": "false", "message": "fail to submit the problem"})
    return jsonify({"success" : "true"})

# Content-Type: application/json;
# body:{"oj", "problem_id", "refresh"}
@judge.route('/problem')
def get_problem():
    data = request.get_json()
    # !!!to be implemented!!!
    # if the problem exist in database && refresh==false, return the problem from database
    # else perform a query and update the database
    oj = OnlineJudge.objects(name=data["oj"]).first()
    problem = Problem.objects(online_judge=oj,problem_id=data["problem_id"]).first()
    if not problem:
        print(data)
        if data["oj"] not in bot_list:
            print("oj in query not found.")
            return jsonify({"success" : "false", "message" : "Invalid OJ name"})
        bot = bot_list[data["oj"]]
        problem_data = bot.get_problem( data["problem_id"])
        problem = Problem(
            online_judge = oj,
            problem_id = data["problem_id"],
            title = problem_data["title"],
            time_limit = problem_data["time_limit"],
            memory_limit = problem_data["memory_limit"],
            description = problem_data["description"],
            input_format = problem_data["input_format"],
            output_format = problem_data["output_format"],
            sample_input = problem_data["sample_input"],
            sample_output = problem_data["sample_output"],
        )
        problem.save()
    return jsonify({"success" : "true"})

@judge.route('/my_submissions')
def my_submissions():
    return "my submissions"

@judge.route('/new_contest')
def new_contest():
    return "new contest"

