from uk_covid19 import Cov19API
import sched
import time
import logging
import json

logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
t = sched.scheduler(time.time, time.sleep)


def parse_csv_data(csv_filename: str) -> list[str]:
    """This function opens the csv file and reads through, splits the lines up, then closes and returns it"""
    # This creates a list
    rows = []
    # This opens and reads the file
    file = open(csv_filename, 'r')
    # This splits the lines of the file into a list
    rows = file.read().splitlines()
    # Closes the file
    file.close()
    return rows


def test_parse_csv_data():
    """This function is used to test the previous function."""
    data = parse_csv_data("nation_2021-10-28.csv")
    assert len(data) == 639


def process_covid_csv_data(covid_csv_data: list[str]) -> tuple[int, int, int]:
    """This function is used to take specific data from the first function and then organise it for later use."""
    last7days_cases = 0
    # This gives me data from the 3rd to the 9th line
    for x in range(3, 10):
        # This removes whitespace and splits the data up into separate sections
        data_list = covid_csv_data[x].strip('\n').split(',')
        # This makes the new value of the variable equal to the CSV file value and converts it to an integer
        last7days_cases = last7days_cases + int(data_list[6])
    data_list = covid_csv_data[1].strip('\n').split(',')
    # This makes the value of the variable equal to the CSV file value and converts it to an integer
    x = 1
    done = False
    while done == False:
        data_list = covid_csv_data[x].strip('\n').split(',')
        # This takes information from the position 5 index by going through the CSV file and reading each line
        # If the line is blank then it will move onto the next line until it has the information
        # Then it will stop reading as it has the necessary information
        if data_list[5] != '':
            current_hospital_cases = int(data_list[5])
            done = True
        x += 1
    x = 1
    done = False
    while done == False:
        data_list = covid_csv_data[x].strip('\n').split(',')
        # This takes information from the position 4 index by going through the CSV file and reading each line
        # If the line is blank then it will move onto the next line until it has the information
        # Then it will stop reading as it has the necessary information
        if data_list[4] != '':
            total_deaths = int(data_list[4])
            done = True
        x += 1
    return last7days_cases, current_hospital_cases, total_deaths


last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))
logging.info(last7days_cases)
logging.info(current_hospital_cases)
logging.info(total_deaths)

def test_process_covid_csv_data():
    """This function is used to test the previous function."""
    last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data\
        (parse_csv_data("nation_2021-10-28.csv"))
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544


def covid_api_request(location='Exeter', location_type='ltla'):
    """This function uses real data by importing it in and outputs it day by day."""
    area_type = 'areaType=' + location_type
    area_name = 'areaName=' + location
    # Interested in local data
    local_only = [area_type, area_name]
    local_cases = {"newCasesBySpecimenDate": "newCasesBySpecimenDate"}
    # Using filters and structure to get specific data
    api = Cov19API(filters=local_only, structure=local_cases)
    local_data = api.get_csv(save_as="Function\\local_data.csv")
    # Interested in England's data so adding a filter
    england_only = [
        'areaType=nation',
        'areaName=England']
    # Setting up the structure for what I plan on getting the data for and showing
    cases_and_deaths = {
        "areaCode": "areaCode",
        "areaName": "areaName",
        "areaType": "areaType",
        "date": "date",
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"}
    # Using filters and structure to initialise the Cov19API object
    api = Cov19API(filters=england_only, structure=cases_and_deaths)
    # Extracting and saving the data
    data = api.get_csv(save_as="Function\\data.csv")


def get_local_data(filepath):
    """This allows me to create a filepath to send my local data to flask"""
    local_7day_cases = 0
    with open(filepath, 'r') as file:
        data = file.readlines()
        for x in range(2, 9):
            local_7day_cases = local_7day_cases + int(data[x].strip('\n'))
        return local_7day_cases

def get_data(filepath):
    """This allows me to create a filepath to send my data to flask"""
    with open(filepath, 'r') as file:
        data = file.readlines()
        last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(data)
        return last7days_cases, current_hospital_cases, total_deaths


def schedule_covid_updates(update_interval, update_name):
    """This function takes the function before and updates it at a given interval"""
    # Setting up the update
    t.enter(update_interval, 1, covid_api_request, argument=("Exeter", "ltla"))
    # Executing the update
    t.run()


# These allow for testing and execution of my functions
test_parse_csv_data()
test_process_covid_csv_data()
covid_api_request('Exeter', 'ltla')
schedule_covid_updates(1, "name")
get_data("Function\\data.csv")