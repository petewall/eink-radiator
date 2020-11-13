# pylint: disable=no-self-use
import os
import json
import unittest
import requests_mock
from hamcrest import assert_that, calling, equal_to, is_, none, raises
from PIL import Image
from image_sources.weather.weather import WeatherContent
from pillow_image_matcher import the_same_image_as


class TestWeatherContent(unittest.TestCase):
    test_fixtures_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', '..', 'test_fixtures'
    )

    def test_missing_api_key(self):
        content = WeatherContent({})
        assert_that(
            calling(content.get_image).with_args((1, 1)),
            raises(ValueError, "API key is required")
        )

    def test_missing_location(self):
        content = WeatherContent({
            'api_key': 'test'
        })
        assert_that(
            calling(content.get_image).with_args((1, 1)),
            raises(ValueError, "Location is required")
        )

    @requests_mock.Mocker()
    def test_get_image(self, request_mock):
        with open(os.path.join('test_fixtures', 'current_weather.json'), 'r') as current_weather:
            with open(os.path.join('test_fixtures', 'forecast.json'), 'r') as forecast:
                content = WeatherContent({
                    'api_key': 'test',
                    'location': '55901'
                })

                request_mock.get(
                    'https://api.openweathermap.org/data/2.5/weather?q=55901&units=imperial&appid=test',
                    json=json.load(current_weather)
                )
                request_mock.get(
                    'https://api.openweathermap.org/data/2.5/forecast?q=55901&units=imperial&appid=test',
                    json=json.load(forecast)
                )

                image, update_interval = content.get_image((400, 300))
                assert_that(update_interval, is_(none()))

                expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'weather.png'))
                assert_that(image, is_(the_same_image_as(expected_image)))
                expected_image.close()

    if __name__ == '__main__':
        unittest.main()
