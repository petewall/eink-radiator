#!/usr/bin/env python
# pylint: disable=line-too-long

import os
import json
from unittest.mock import patch
import requests_mock
from image_sources.blank import Red, White
from image_sources.image import ImageContent
from image_sources.text import TextContent
from image_sources.weather.weather import WeatherContent

def generate_blank():
    content = Red()
    image, _ = content.get_image((400, 300))
    image.save(os.path.join('test_fixtures', 'blank_red.png'))

    content = White()
    image, _ = content.get_image((400, 300))
    image.save(os.path.join('test_fixtures', 'blank_white.png'))

def generate_image():
    source_image = open(os.path.join('test_fixtures', 'InkywHAT-400x300.png'), 'rb')
    with patch('urllib.request.urlopen', return_value=source_image):
        content = ImageContent({
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'scale': 'contain'
        })
        image, _ = content.get_image((200, 300))
        image.save(os.path.join('test_fixtures', 'image_contained_tall.png'))

        image, _ = content.get_image((400, 200))
        image.save(os.path.join('test_fixtures', 'image_contained_wide.png'))

        content.set_configuration({'scale': 'cover'})
        image, _ = content.get_image((200, 300))
        image.save(os.path.join('test_fixtures', 'image_covered_tall.png'))

        image, _ = content.get_image((400, 200))
        image.save(os.path.join('test_fixtures', 'image_covered_wide.png'))

        content.set_configuration({'scale': 'scale'})
        image, _ = content.get_image((200, 200))
        image.save(os.path.join('test_fixtures', 'image_scaled.png'))

def generate_text():
    content = TextContent({
        'text': 'It is now safe to turn off your computer'
    })
    image, _ = content.get_image((400, 300))
    image.save(os.path.join('test_fixtures', 'text_1.png'))

    content.set_configuration({
        'name': 'Test Image',
        'text': 'Shields up! Rrrrred alert!',
        'foreground_color': 'red',
        'background_color': 'black',
        'superfluous': 'not relevant'
    })
    image, _ = content.get_image((400, 300))
    image.save(os.path.join('test_fixtures', 'text_2.png'))

    content.set_configuration({
        'text': 'Docker engineers\ndo it in a container',
        'foreground_color': 'white',
        'background_color': 'black'
    })
    image, _ = content.get_image((400, 300))
    image.save(os.path.join('test_fixtures', 'text_3.png'))

def generate_weather():
    with requests_mock.Mocker() as request_mock:
        with open(os.path.join('test_fixtures', 'current_weather.json'), 'r') as current_weather:
            with open(os.path.join('test_fixtures', 'forecast.json'), 'r') as forecast:
                content = WeatherContent({
                    'api_key': 'test',
                    'location': '55901'
                })

                request_mock.get(
                    'https://api.openweathermap.org/data/2.5/weather?q=55901&units=imperial&appid=test',
                    json=json.load(current_weather))
                request_mock.get(
                    'https://api.openweathermap.org/data/2.5/forecast?q=55901&units=imperial&appid=test',
                    json=json.load(forecast))

                image, _ = content.get_image((400, 300))
                image.save(os.path.join('test_fixtures', 'weather.png'))

generate_blank()
generate_image()
generate_text()
generate_weather()
