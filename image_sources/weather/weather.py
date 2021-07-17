import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests
from image_sources.image_source import ImageSource
from color import Color

FONT_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..', 'RobotoSlab-Regular.ttf'
)

day_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']


def get_x_position(element_width, canvas_width, offset=0):
    return int((canvas_width - element_width) / 2) + offset


class WeatherContent(ImageSource):
    api_key = None
    location = None
    unit = 'imperial'

    location_font = ImageFont.truetype(font=FONT_PATH, size=16)
    temp_font = ImageFont.truetype(font=FONT_PATH, size=100)
    condition_font = ImageFont.truetype(font=FONT_PATH, size=24)
    forecast_font = ImageFont.truetype(font=FONT_PATH, size=16)

    def __init__(self, params):
        if params.get('interval') is None:
            params['interval'] = 3600
        super().__init__(params)

    def get_configuration(self):
        return {
            **super().get_configuration(),
            **{
                'name': self.name,
                'api_key': self.api_key,
                'location': self.location
            }
        }

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('api_key') is not None:
            self.api_key = params.get('api_key')
        if params.get('location') is not None:
            self.location = params.get('location')

    def build_weather_url(self, path):
        return f'https://api.openweathermap.org/data/2.5/{path}' + \
            f'?q={self.location}&units={self.unit}&appid={self.api_key}'

    def get_weather(self):
        current = requests.get(self.build_weather_url('weather'))
        if current.status_code != 200:
            raise RuntimeError(f'Failed to get current\nweather for {self.location}:\n' + \
                f'{current.status_code}: {current.text}')
        forecast = requests.get(self.build_weather_url('forecast'))
        if forecast.status_code != 200:
            raise RuntimeError(f'Failed to get weather\nforecast for {self.location}:\n' + \
                f'{forecast.status_code}: {forecast.text}')
        return current.json(), forecast.json()

    def make_image(self, size) -> Image:
        #pylint: disable=invalid-name,too-many-locals
        if self.api_key is None or self.api_key == '':
            raise ValueError('API key is required')
        if self.location is None or self.location == '':
            raise ValueError('Location is required')

        current, forecast = self.get_weather()

        (width, height) = size
        image = Image.new('P', (width, height), Color.WHITE.value)
        image.putpalette(Color.palette())
        image_canvas = ImageDraw.Draw(image)

        city = current['name']
        text_width, text_height = image_canvas.textsize(city, font=self.location_font)
        x = get_x_position(text_width, width)
        y = 10
        image_canvas.text((x, y), city, fill=Color.BLACK.value, font=self.location_font)

        y += text_height + 10
        image_canvas.line([(0, y), (width, y)], fill=Color.BLACK.value, width=3)

        current_temp = f'{int(current["main"]["temp"])}º'
        text_width, text_height = image_canvas.textsize(current_temp, font=self.temp_font)
        x = get_x_position(text_width, width)
        image_canvas.text((x, y), current_temp, fill=Color.BLACK.value, font=self.temp_font)

        description = current['weather'][0]['description']
        y += text_height + 15
        text_width, text_height = image_canvas.textsize(description, font=self.condition_font)
        x = get_x_position(text_width, width)
        image_canvas.text((x, y), description, fill=Color.BLACK.value, font=self.condition_font)

        step = int(24 / 3)  # 3 hour forecast
        days_in_forecast = int(len(forecast['list']) / step)
        for i in range(0, len(forecast['list']), step):
            date = datetime.fromtimestamp(
                forecast['list'][i]['dt'] - forecast['city']['timezone']
            )
            low = f'{int(forecast["list"][i]["main"]["temp_min"])}º'
            high = f'{int(forecast["list"][i]["main"]["temp_max"])}º'
            day = day_of_week[date.weekday()]

            column_width = size[0] / days_in_forecast
            column_offset = (column_width) * i / step

            text_width, text_height = image_canvas.textsize(low, font=self.forecast_font)
            x = get_x_position(text_width, column_width, column_offset)
            y = height - (text_height + 10)
            image_canvas.text((x, y), low, fill=Color.BLACK.value, font=self.forecast_font)

            y -= (text_height + 2)
            text_width, text_height = image_canvas.textsize(high, font=self.forecast_font)
            x = get_x_position(text_width, column_width, column_offset)
            image_canvas.text((x, y), high, fill=Color.RED.value, font=self.forecast_font)

            y -= (text_height + 2)
            text_width, text_height = image_canvas.textsize(day, font=self.forecast_font)
            x = get_x_position(text_width, column_width, column_offset)
            image_canvas.text((x, y), day, fill=Color.BLACK.value, font=self.forecast_font)

        y = height - 70
        image_canvas.line([(0, y), (width, y)], fill=Color.BLACK.value, width=3)

        return image
