import os

import requests
from dotenv import load_dotenv

load_dotenv('../.env')


def get_weather_in_city():
    city = input('Input city: ')
    url = 'https://api.openweathermap.org/data/2.5/weather'
    appid = os.getenv('OPEN_WEATHER_TOKEN', None)
    params = {'q': city, 'appid': appid}
    response = requests.get(url=url, params=params)
    data = response.json()
    if response.status_code == 200:
        weather = {
            'weather_name': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'main': data['main'],
            'city': data['name'],
            'wind': data['wind'],
        }
        return f"In {weather['city']} {weather['weather_name']}({weather['description']}).\n" \
               f"Main: {weather['main']}\nWind: {weather['wind']}"
    return f'{response.status_code}'
