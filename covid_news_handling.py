import requests
import time
import sched
import json
import logging

logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
s = sched.scheduler(time.time, time.sleep)


def news_api_request(covid_terms="Covid COVID-19 coronavirus"):
    """This function searches for all news headlines to do with covid and prints them out"""
    # Setting up the beginning of the url
    base_url = "https://newsapi.org/v2/everything?qInTitle="
    # Adding my API key
    api_key = "9d3139875c9a446e88d362e823d03019"
    # Setting the language of the articles to English
    language = "en"
    # Creating the full url
    complete_url = base_url + ' OR '.join(covid_terms.split(' ')) + "&language=" + language + "&apiKey=" + api_key
    response = requests.get(complete_url)
    json_data = response.json()
    logging.info(json_data)
    # The following allows me to take this info and use it for the Flask section
    global news
    news = response.json()
    file = open('Function\\news.json', 'w')
    file = json.dump(json_data, file)
    return json_data

# This will be used in the flask section
def find_news(filepath):
    """This allows me to create a filepath to send my data to flask"""
    with open(filepath, 'r') as file:
        news_dict = json.load(file)
        articles = news_dict['articles']
        return articles


def update_news(update_time):
    """This function takes the first function  and updates it at a given interval"""
    # Setting up the update
    s.enter(update_time, 3, news_api_request)
    # Executing the update
    s.run()


# These allow for updating and execution of my functions
news_api_request()
update_news(3)
