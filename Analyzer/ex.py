from flask import Flask, redirect, render_template, request
import math
import requests
from datetime import datetime
from random import randint
from flask import render_template_string


app = Flask(__name__)

app.jinja_env.filters['date'] = lambda timestamp: datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

app.jinja_env.filters['timestamp_to_datetime'] = lambda timestamp: datetime.utcfromtimestamp(timestamp)

@app.template_filter('timestamp_to_datetime')
def timestamp_to_datetime(timestamp, format='%Y-%m-%d %H:%M:%S'):
    return datetime.utcfromtimestamp(timestamp).strftime(format)

def get_user_info(handle):
    url = f'https://codeforces.com/api/user.info?handles={handle}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    try:
        user_info = data['result'][0]
        return user_info
    except (KeyError, IndexError):
        return None

def get_submission_data(handle):
    url = f'https://codeforces.com/api/user.status?handle={handle}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return None

    data = response.json()
    ratings = []
    correct_answers = 0
    wrong_answers = 0
    
    for element in data['result']:
        try:
            if element['verdict'] == 'OK':
                ratings.append(element['problem']['rating'])
                correct_answers += 1
            else:
                wrong_answers += 1
        except:
            continue
    
    rating_occurrence = {rate: ratings.count(rate) for rate in ratings}
    rating_occurrence = dict(sorted(rating_occurrence.items()))
    x = [item for item in rating_occurrence]
    y = [rating_occurrence[idx] for idx in rating_occurrence]
    
    return x, y, correct_answers, wrong_answers

# Add this function to fetch upcoming contests
def get_upcoming_contests():
    url = 'https://codeforces.com/api/contest.list?gym=false'
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    upcoming_contests = []

    for contest in data['result']:
        if contest['phase'] == 'BEFORE':
            contest_info = {
                'name': contest['name'],
                'startTimeSeconds': contest['startTimeSeconds'],
            }
            upcoming_contests.append(contest_info)
    upcoming_contests.sort(key=lambda x: x['startTimeSeconds'])    
    return upcoming_contests


def get_number(query):
    res = input(query)
    while True:
        try:
            res = int(res)
            # Check if it is a valid difficulty (multiple of 100)
            if (res % 100) != 0:
                raise Exception
            break
        except:
            res = input("Not a valid number. Make sure it is a multiple of 100. " + query)
    return res

def get_tags():
    print("Enter optional problem tags:")
    tags = []
    while True:
        q = input("Enter problem tag (or nothing to stop): ")
        if q == "":
            break
        tags.append(q)
    return tags

def get_problems(lower_bound, upper_bound, tags):
    url = "https://codeforces.com/api/problemset.problems?tags=" + ";".join(tags)
    res = requests.get(url).json()

    if res["status"] == "FAILED":
        print("Request returned with FAILED status. Exiting...")
        quit()

    problems = res["result"]["problems"]
    filtered_problems = []

    for problem in problems:
        if "rating" not in problem:
            continue
        if lower_bound <= problem["rating"] <= upper_bound:
            filtered_problems.append(problem)

    return filtered_problems

def random_problem(problems):
    idx = randint(0, len(problems) - 1)
    return {
        "name": problems[idx]["name"],
        "url": f"https://codeforces.com/problemset/problem/{problems[idx]['contestId']}/{problems[idx]['index']}"
    }

def get_contest_data(handle):
    url = f'https://codeforces.com/api/user.rating?handle={handle}'
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    contests = data['result']

    if not contests:
        return None

    best = float('inf')
    worst = float('-inf')
    max_up = 0
    max_down = 0
    best_con = ''
    worst_con = ''
    max_up_con = ''
    max_down_con = ''
    total_contests = len(contests)
    contest_data = []

    for con in contests:
        rank = con.get('rank', 0)
        if rank < best:
            best = rank
            best_con = con['contestId']
        if rank > worst:
            worst = rank
            worst_con = con['contestId']

        change = con['newRating'] - con['oldRating']
        if change > max_up:
            max_up = change
            max_up_con = con['contestId']
        if change < max_down:
            max_down = change
            max_down_con = con['contestId']

        contest_info = {
            'contestId': con['contestId'],
            'rank': rank,
            'newRating': con['newRating'],
            'oldRating': con['oldRating'],
            'change': change,
            'contestName': con.get('contestName', ''),
            'startTimeSeconds': con.get('ratingUpdateTimeSeconds', 0),
        }
        contest_data.append(contest_info)

    contest_data.sort(key=lambda x: x['startTimeSeconds'])

    return contest_data



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        user_info = get_user_info(username)
        if user_info:
            [rating, count, correct_answers, wrong_answers] = get_submission_data(username)
            upcoming_contests = get_upcoming_contests()
            return render_template('results.html', user_info=user_info, rating=rating, count=count,
                                   correct_answers=correct_answers, wrong_answers=wrong_answers,
                                   upcoming_contests=upcoming_contests)
        else:
            return render_template('error.html', message='User not found or unable to fetch information.')
    return render_template('index.html')

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    print("Inside /compare route")
    if request.method == 'POST':
        username1 = request.form['username1']
        username2 = request.form['username2']





#Codeforces data retrieval
        user_info1 = get_user_info(username1)
        user_info2 = get_user_info(username2)

        if user_info1 and user_info2:
            [rating1, count1, correct_answers1, wrong_answers1] = get_submission_data(username1)
            [rating2, count2, correct_answers2, wrong_answers2] = get_submission_data(username2)

            return render_template('compare_results.html',
                                   user_info1=user_info1,
                                   user_info2=user_info2,
                                   rating1=rating1,
                                   count1=count1,
                                   correct_answers1=correct_answers1,
                                   wrong_answers1=wrong_answers1,
                                   rating2=rating2,
                                   count2=count2,
                                   correct_answers2=correct_answers2,
                                   wrong_answers2=wrong_answers2)
        else:
            return render_template('error.html', message='One or both Codeforces users not found or unable to fetch information.')
    return redirect('/')

@app.route('/random', methods=['GET', 'POST'])
def random():
    if request.method == 'POST':
        lower_bound = get_number("Enter lower difficulty bound (inclusive): ")
        upper_bound = get_number("Enter upper difficulty bound (inclusive): ")
        tags = get_tags()

        problems = get_problems(lower_bound, upper_bound, tags)

        if problems:
            random_problem_info = random_problem(problems)
            return render_template('random_problem.html', random_problem_info=random_problem_info)
        else:
            return render_template('error.html', message='No problems found within the specified criteria.')

    return render_template('/')

@app.route('/contest', methods=['GET', 'POST'])
def contest():
    if request.method == 'POST':
        username = request.form['username']
        user_info = get_user_info(username)
        if user_info:
            contest_data = get_contest_data(username)
            problems_data = get_submission_data(username)  # Modify this function if needed
            return render_template_string('results.html', user_data=contest_data, problems_data=problems_data, user_info=user_info)
        else:
            return render_template_string('error.html', message='User not found or unable to fetch information.')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

'''
<h1>Random Problem Input</h1>

    <form method="post" action="/random">
        <label for="lower_bound">Enter lower difficulty bound (inclusive):</label>
        <input type="number" id="lower_bound" name="lower_bound" required>

        <label for="upper_bound">Enter upper difficulty bound (inclusive):</label>
        <input type="number" id="upper_bound" name="upper_bound" required>

        <label for="tags">Enter optional problem tags (comma-separated):</label>
        <input type="text" id="tags" name="tags">

        <button type="submit">Get Random Problem</button>
    </form>
'''