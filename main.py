import requests
from datetime import datetime
import pandas as pd
import os

#--------------------------------create a time-------------------------------------------#

today = datetime.now()
year = today.strftime("%x")
time_ = today.strftime("%X")

#-------------------------------POST and respons info exercises--------------------------#
APP_ID = os.environ['APP_ID']
API_KEY = os.environ['API_KEY']
NUTRITIONIX_API_ENDPOINT = 'https://trackapi.nutritionix.com/v2/natural/exercise'

param_conf = {
    'query':input('Tell as which exercises you did: '),
    'weight_kg': 66,
    'height_cm': 170,
    'age': 29,
}
header = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
}

response_nutritionix = requests.post(url=NUTRITIONIX_API_ENDPOINT, json=param_conf, headers=header)
response_nutritionix.raise_for_status()
data_exercise = response_nutritionix.json()['exercises']

#---------------------- get-post-sheets doc-----------------------------------------------#
SHEETS_API = os.environ['SHEETS_API']
BASIC_AUTH = os.environ['BASIC_AUTH']
URL_SHEETS = f'https://api.sheety.co/{SHEETS_API}/myWorkouts/workouts'
headers = {
    "Authorization": f'{BASIC_AUTH}'
}
# response_sheets = requests.get(url=URL_SHEETS)
# data_sheets = response_sheets.json()

#--------------------------add exercises in sheets------------------------------------------#
for info in data_exercise:
    exercises = info['name'].title()
    duration_min = info['duration_min']
    calories = info['nf_calories']
    dict_exercises = {
            'workout': {'date': year, 'time': time_, 'exercise': exercises,
                          'duration': duration_min, 'calories': calories, 'id': 2}
        }

    response_sheets_add = requests.post(url=URL_SHEETS,json=dict_exercises, headers=headers)
    print(response_sheets_add.text)