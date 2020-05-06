import os
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont
import requests
from image_sources.image_source import ImageSource
from color import Color

FONT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'RobotoSlab-Regular.ttf')

day_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']


def get_x_position(element_width, canvas_width, offset=0):
    return int((canvas_width - element_width) / 2) + offset


class WeatherContent(ImageSource):
    api_key = None
    location = None
    unit = 'imperial'

    location_font = ImageFont.truetype(font=FONT_PATH, size=16)
    temperature_font = ImageFont.truetype(font=FONT_PATH, size=100)
    condition_font = ImageFont.truetype(font=FONT_PATH, size=24)
    forecast_font = ImageFont.truetype(font=FONT_PATH, size=16)

    def get_configuration(self):
        return {
            'name': self.name,
            'api_key': self.api_key,
            'location': self.location
        }

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('api_key') is not None:
            self.api_key = params.get('api_key')
        if params.get('location') is not None:
            self.location = params.get('location')

    def build_weather_url(self, path):
        return f'https://api.openweathermap.org/data/2.5/{path}?q={self.location}&units={self.unit}&appid={self.api_key}'

    def get_weather(self):
        current = requests.get(self.build_weather_url('weather'))
        if current.status_code != 200:
            raise RuntimeError(f'Failed to get current\nweather for {self.location}:\n{current.status_code}: {current.text}')

        forecast = requests.get(self.build_weather_url('forecast'))
        if forecast.status_code != 200:
            raise RuntimeError(f'Failed to get weather\nforecast for {self.location}:\n{forecast.status_code}: {forecast.text}')
        return current.json(), forecast.json()

    def get_image(self, size):
        if self.api_key is None or self.api_key == '':
            raise ValueError('API key is required')
        if self.location is None or self.location == '':
            raise ValueError('Location is required')

        current, forecast = self.get_weather()

        (width, height) = size
        image = Image.new('P', (width, height), Color.white.value)
        image.putpalette(Color.palette())
        image_canvas = ImageDraw.Draw(image)

        text_width, text_height = image_canvas.textsize(current['name'], font=self.location_font)
        x_pos = get_x_position(text_width, width)
        y_pos = 10
        image_canvas.text((x_pos, y_pos), current['name'], fill=Color.black.value, font=self.location_font)

        y_pos += text_height + 10
        image_canvas.line([(0, y_pos), (width, y_pos)], fill=Color.black.value, width=3)

        current_temp = f'{int(current["main"]["temp"])}º'
        text_width, text_height = image_canvas.textsize(current_temp, font=self.temperature_font)
        x_pos = get_x_position(text_width, width)
        image_canvas.text((x_pos, y_pos), current_temp, fill=Color.black.value, font=self.temperature_font)

        y_pos += text_height + 15
        text_width, text_height = image_canvas.textsize(current['weather'][0]['description'], font=self.condition_font)
        x_pos = get_x_position(text_width, width)
        image_canvas.text((x_pos, y_pos), current['weather'][0]['description'], fill=Color.black.value, font=self.condition_font)

        step = int(24 / 3)  # 3 hour forecast
        days_in_forecast = int(len(forecast['list']) / step)
        for i in range(0, len(forecast['list']), step):
            date = datetime.fromtimestamp(forecast['list'][i]['dt'] - forecast['city']['timezone'])
            low = f'{int(forecast["list"][i]["main"]["temp_min"])}º'
            high = f'{int(forecast["list"][i]["main"]["temp_max"])}º'
            day = day_of_week[date.weekday()]

            text_width, text_height = image_canvas.textsize(low, font=self.forecast_font)
            x_pos = get_x_position(text_width, size[0] / days_in_forecast, (size[0] / days_in_forecast) * i / step)
            y_pos = height - (text_height + 10)
            image_canvas.text((x_pos, y_pos), low, fill=Color.black.value, font=self.forecast_font)

            y_pos -= (text_height + 2)
            text_width, text_height = image_canvas.textsize(high, font=self.forecast_font)
            x_pos = get_x_position(text_width, size[0] / days_in_forecast, (size[0] / days_in_forecast) * i / step)
            image_canvas.text((x_pos, y_pos), high, fill=Color.red.value, font=self.forecast_font)

            y_pos -= (text_height + 2)
            text_width, text_height = image_canvas.textsize(day, font=self.forecast_font)
            x_pos = get_x_position(text_width, size[0] / days_in_forecast, (size[0] / days_in_forecast) * i / step)
            image_canvas.text((x_pos, y_pos), day, fill=Color.black.value, font=self.forecast_font)

        y_pos = height - 70
        image_canvas.line([(0, y_pos), (width, y_pos)], fill=Color.black.value, width=3)

        return image
