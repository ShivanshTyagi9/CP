import random
from flask import Flask, redirect, render_template, request
import requests
from datetime import datetime, timezone
from flask import render_template_string

app = Flask(__name__)

app.jinja_env.filters['date'] = lambda timestamp: datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

@app.template_filter('timestamp_to_datetime')
def timestamp_to_datetime(timestamp, format='%Y-%m-%d %H:%M:%S'):
    return datetime.fromtimestamp(timestamp, timezone.utc).strftime(format)

def get_user_info(handle):
    url = f'https://codeforces.com/api/user.info?handles={handle}'
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    try:
        user_info = data['result'][0]
        user_info['profile_picture'] = f'https:{user_info.get("avatar", "/path/to/default/avatar")}'
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
    sub_info = {
            'total_contests': total_contests,
            'best_con': best_con,
            'worst_con': worst_con,
            'max_up_con': max_up_con,
            'max_down_con': max_down_con,
        }
    contest_data.append(sub_info)

    return contest_data

def get_unsolved_problems(handle):
    url = f'https://codeforces.com/api/user.status?handle={handle}'
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    unsolved_problems = set()  # Use a set to store unique problems

    for element in data['result']:
        try:
            if element['verdict'] != 'OK':
                problem_id = f"{element['contestId']}-{element['problem']['index']}"
                unsolved_problems.add(problem_id)
        except:
            continue

    return list(unsolved_problems)

    
    

def get_random_problem(difficulty):
    url = f'https://codeforces.com/api/problemset.problems'
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    problems = data['result']['problems']

    filtered_problems = [problem for problem in problems if 'rating' in problem and problem['rating'] == difficulty]

    if not filtered_problems:
        return None

    random_problem = random.choice(filtered_problems)

    return {
        'contestId': random_problem['contestId'],
        'problemIndex': random_problem['index'],
        'name': random_problem.get('name', ''),
        'rating': random_problem.get('rating', 0),
        'tags': random_problem.get('tags','')
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        user_info = get_user_info(username)
        if user_info:
            [rating, count, correct_answers, wrong_answers] = get_submission_data(username)
            upcoming_contests = get_upcoming_contests()
            contest_data = get_contest_data(username)
            sub_info = contest_data[-1]
            unsolved_problems = get_unsolved_problems(username)
            return render_template('results.html', user_info=user_info, rating=rating, count=count,
                                   correct_answers=correct_answers, wrong_answers=wrong_answers,
                                   upcoming_contests=upcoming_contests, contest_data=contest_data, sub_info=sub_info, unsolved_problems=unsolved_problems)
        else:
            return render_template('error.html', message='User not found or unable to fetch information.')
    return render_template('index.html')

@app.route('/random', methods=['GET', 'POST'])
def random_prob():
    if request.method == 'POST':
        difficulty = int(request.form.get('difficulty')) 
        random_problem = get_random_problem(difficulty)
        if random_problem:
            return render_template('results.html', random_problem=random_problem)
        else:
            return render_template('error.html', message='Unable to fetch information.')
    return render_template('index.html')    


if __name__ == "__main__":
    app.run(debug=True)
