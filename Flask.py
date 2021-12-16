from flask import Flask, render_template, redirect
from flask import request
from covid_news_handling import find_news, news_api_request
from covid_data_handler import covid_api_request, get_data, get_local_data
import sched
import time
import logging

logging.basicConfig(filename='logging.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)

# This is where the news articles will go into
news = {}


@app.route('/')
def url_redirect():
    """This redirects the webpage back to the covid data webpage"""
    app.logger.info('Processing default request')
    # The name of the website
    return redirect('/index')


@app.route('/index')
def webpage():
    """This imports the functions from other modules and outputs the data onto the webpage"""
    # This outputs the news articles
    articles = find_news('Function\\news.json')
    # This outputs the national statistics
    last7days_cases, current_hospital_cases, total_deaths = get_data('Function\\data.csv')
    # This outputs the local statistics
    local_7day_cases = get_local_data('Function\\local_data.csv')
    # This affects what appears on the website
    return render_template('index.html',
                           news_articles=articles, nation_location='England', national_7day_infections=last7days_cases,
                           hospital_cases='Hospital Cases: '+str(current_hospital_cases),
                           deaths_total='Total Deaths: '+str(total_deaths), title='Daily Update', location='Exeter',
                           local_7day_infections=local_7day_cases, image='Health.png')


def add_news_article():
    """This will add additional news articles"""
    news.append({
        "title": "t",
        "content": "c"
    })


def schedule_add_news():
    """Adds new article at given interval"""
    s.enter(1, 1, add_news_article)


def minutes_to_seconds(minutes: str) -> int:
    """Time conversion"""
    return int(minutes)*60


def hours_to_minutes(hours: str) -> int:
    """Time conversion"""
    return int(hours)*60


def hhmm_to_seconds(hhmm: str) -> int:
    """Time conversion"""
    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + minutes_to_seconds(hhmm.split(':')[1])


@app.route('/index')
def index():
    """This will ask for a value for when scheduling an update"""
    s.run(blocking=False)
    text_field = request.args.get("two")
    print(text_field)
    if text_field:
        update_time = request.args.get("update")
        print(update_time)
        update_time_sec = hhmm_to_seconds(update_time)
        schedule_add_news(update_time_sec)
    return render_template('index.html')


if __name__ == '__main__':
    e1 = s.enter(1, 1, covid_api_request)
    e2 = s.enter(2, 2, news_api_request)
    s.run()
    app.run()
