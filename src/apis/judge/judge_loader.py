import re
import requests
from apis.models import *

class loader(object):
    def __init__(self):
        pass


class codeforces_loader(loader):
    # establish connection with server. note that a CSRF token acquired from any page is needed before login.
    def __init__(self):
        self.cookies = None
        self.csrf_token = None
        response = requests.get("http://codeforces.com/enter")
        self.cookies = response.cookies
        self.update_csrf_token(response)
        self.login()
        # should be acquired from database
        self.user_name = "zhonghas"
        self.password = "" # should be in database
        pass

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

    # in the form "https://codeforces.com/contest/1143/problem/A"
    def construct_problem_url(self, contest, problem_id):
        return "https://codeforces.com/problemset/problem/" + str(contest) + "/" + str(problem_id)

    def parse_problem(self, text):
        title = re.compile(r'<div class="title">(.+?)</div>').findall(text)[0]
        print(title)

    def get_problem(self, contest, problem_id):
        url = self.construct_problem_url(contest,problem_id)
        response = requests.get(url)
        self.parse_problem(response.text)

    # add a submission to database
    def submit(self, language, code, contest, problem_id):
        url = self.construct_problem_url(contest, problem_id)
        response = requests.post(url,
                                 files=
                                 {
                                     "csrf_token": self.csrf_token,
                                     "action": "submitsolutionformsubmitted",
                                     "submittedProblemIndex": "A",
                                     "source": code,
                                     "programTypeId": language,
                                 },
                                 cookies=self.cookies
                                 )
        print(response)

    def get_result_list(self):
        last_result = 0
        request_url = "https://codeforces.com/api/user.status?handle=" + self.user_name + "&from=" + str(last_result)
        response = requests.get(request_url)
        result_list = response.json()["result"]
        for result in result_list:
            print(result['id'], result['programmingLanguage'], result['verdict'],
                  result['timeConsumedMillis'], result['memoryConsumedBytes'])