import re
import requests
from apis.models import *

class bot(object):
    def __init__(self):
        pass


class codeforces_bot(bot):
    # establish connection with server. note that a CSRF token acquired from any page is needed before login.
    def __init__(self):
        # should be acquired from database
        self.user_name = "zhonghas"
        self.password = "" # should be in database

        self.cookies = None
        self.csrf_token = None
        response = requests.get("http://codeforces.com/enter")
        self.cookies = response.cookies
        self.update_csrf_token(response)
        self.login()

    def update_csrf_token(self,response):
        self.csrf_token = re.compile(r'<meta name="X-Csrf-Token" content="([0-9a-f]+)"/>').findall(response.text)[0]

    # the CSRF token needs to be updated for future authentication
    def login(self):
        response = requests.post("https://codeforces.com/enter",
                                 data=
                                 {
                                     "csrf_token": self.csrf_token,
                                     "action": "enter",
                                     "handleOrEmail": self.user_name,
                                     "password": self.password,
                                     "remember": "on"
                                 },
                                 cookies=self.cookies
                                 )
        self.update_csrf_token(response)
        print("login response: ", response)

    # in the form "https://codeforces.com/contest/1143/problem/A"
    def construct_problem_url(self, contest, id):
        return "https://codeforces.com/problemset/problem/" + str(contest) + "/" + str(id)

    def parse_problem_id(self, problem_id):
        contest, id = "", ""
        try:
            contest, id = re.compile("^(\d+)([a-zA-Z])$").findall(problem_id)[0]
            print(contest, id)
        except:
            print("not a valid problem id")
        return contest, id

    def parse_problem(self, text):
        parse_result = {}
        try:
            parse_result["title"] = re.compile(r'<div class="title">(.+?)</div>').findall(text)[0]
            parse_result["time_limit"] = re.compile(r'<div class="time-limit"><div class="property-title">.+?</div>(.+?)</div>').findall(text)[0]
            parse_result["memory_limit"] = re.compile(r'<div class="memory-limit"><div class="property-title">.+?</div>(.+?)</div>').findall(text)[0]

            print(parse_result["title"] )
        except:
            print("not a valid problem page")

        return parse_result

    def get_problem(self, problem_id):
        contest, id = self.parse_problem_id(problem_id)
        url = self.construct_problem_url(contest,id)
        response = requests.get(url)
        return self.parse_problem(response.text)

    # add a submission to database
    def submit(self, problem_id, language, code):
        contest, id = self.parse_problem_id(problem_id)
        url = self.construct_problem_url(contest, id)
        response = requests.post(url,
                                 files=
                                 {
                                     "csrf_token": self.csrf_token,
                                     "action": "submitsolutionformsubmitted",
                                     "submittedProblemIndex": id,
                                     "source": code,
                                     "programTypeId": language,
                                 },
                                 cookies=self.cookies
                                 )
        print(response)
        return response.status_code

    def get_result_list(self):
        last_result = 0
        request_url = "https://codeforces.com/api/user.status?handle=" + self.user_name + "&from=" + str(last_result)
        response = requests.get(request_url)
        result_list = response.json()["result"]
        for result in result_list:
            print(result['id'], result['programmingLanguage'], result['verdict'],
                  result['timeConsumedMillis'], result['memoryConsumedBytes'])