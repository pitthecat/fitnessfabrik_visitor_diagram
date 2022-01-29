#!/usr/bin/python3
import requests
import datetime
import logging
import csv
import time
import os.path
from bs4 import BeautifulSoup # pip3 install beautifulsoup4
import pandas as pd # pip3 install pandas
import plotly.express as px # pip3 install plotly
import plotly
import shutil

logging.basicConfig(filename='get_visior_count.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

script_path = os.path.abspath(os.getcwd())
url = 'http://besucher.fitnessfabrik.de/'
todays_date = datetime.datetime.now().date()
gym_count_table_position = 2 # my local gym studio (Darmstadt) in the HTML table
file_name = '{}/{}.csv'.format(script_path,todays_date)
file_name_plot = '{}/{}.html'.format(script_path,todays_date)

# Functions
def get_current_activity():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        current_count = soup.findAll('td')[gym_count_table_position].string.strip()
        logging.info("Current count: {}".format(current_count))
        return current_count
    except:
        logging.error("Couldn't get current count")

def write_to_file():
    current_time = datetime.datetime.now()
    ISO_8601_time = current_time.isoformat()
    try:
        current_count = get_current_activity()
        with open(file_name, mode='a') as activity_status:
            activity_status_writer = csv.writer(activity_status, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            activity_status_writer.writerow([ISO_8601_time, current_count])
            print(ISO_8601_time, current_count)
    except:
        logging.error("Error: Count variable emtpy")

def create_document_for_today():
    with open(file_name.format(file_name), mode='w') as activity_status:
        activity_status_writer = csv.writer(activity_status, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        activity_status_writer.writerow(["time","count"])

def create_graph():
    plot_file = pd.read_csv(file_name)
    fig = px.line(plot_file, x = 'time', y = 'count', title='Fitnessfabrik Eschollbrücker Besucherzahlen')
    plotly.offline.plot(fig, filename=file_name_plot)

def copy_graph():
    shutil.copy2(file_name_plot, '/var/www/html/{}.html'.format(todays_date)) # The user running the scripts needs the correct permission for the dir

def run_all():
    while True:
        write_to_file()
        create_graph()
        #copy_graph()
        time.sleep(60)

# Run

if os.path.isfile(file_name_plot):
    logging.info("File for today already exists")
    run_all()
else:
    logging.info("No file for today - Creating...")
    create_document_for_today()
    run_all()