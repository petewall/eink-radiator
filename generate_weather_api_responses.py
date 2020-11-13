#!/usr/bin/env python

import json
import os
import sys
import requests
from image_sources.weather.weather import WeatherContent

content = WeatherContent({
    'api_key': sys.argv[1],
    'location': '55901'
})

current_weather = requests.get(content.build_weather_url('weather'))
with open(os.path.join('test_fixtures', 'current_weather.json'), 'w') as f:
    json.dump(current_weather.json(), f)

forecast = requests.get(content.build_weather_url('forecast'))
with open(os.path.join('test_fixtures', 'forecast.json'), 'w') as f:
    json.dump(forecast.json(), f)
