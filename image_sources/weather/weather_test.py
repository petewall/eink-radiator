import os
from io import BytesIO
import unittest
from requests import Response
from unittest.mock import call, patch
from hamcrest import assert_that, calling, equal_to, has_entries, is_, raises
from PIL import Image
from image_sources.weather.weather import WeatherContent


class TestWeatherContent(unittest.TestCase):
    test_fixtures_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', '..', 'test_fixtures'
    )

    def test_missing_api_key(self):
        content = WeatherContent({})
        assert_that(calling(content.get_image).with_args((1, 1)), raises(ValueError, "API key is required"))

    def test_missing_location(self):
        content = WeatherContent({
            'api_key': 'test'
        })
        assert_that(calling(content.get_image).with_args((1, 1)), raises(ValueError, "Location is required"))

    def test_get_image(self):
        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'weather.png'))

        content = WeatherContent({
            'api_key': 'test',
            'location': '55901'
        })

        current = Response()
        current._content = """
        {
            "name": "Rochester",
            "main": {
                "temp": 68
            },
            "weather": [{
                "description": "perfect"
            }]
        }
        """.encode()
        current.status_code = 200
        forecast = Response()
        forecast._content = """
        {
            "city": {
                "timezone": -18000                
            },
            "list": [
                {"dt": 1588874400, "main": {"temp_min": 0, "temp_max": 10}}, {}, {}, {}, {}, {}, {}, {},
                {"dt": 1588960800, "main": {"temp_min": 10, "temp_max": 20}}, {}, {}, {}, {}, {}, {}, {},
                {"dt": 1589047200, "main": {"temp_min": 20, "temp_max": 30}}, {}, {}, {}, {}, {}, {}, {},
                {"dt": 1589133600, "main": {"temp_min": 30, "temp_max": 40}}, {}, {}, {}, {}, {}, {}, {},
                {"dt": 1589220000, "main": {"temp_min": 40, "temp_max": 50}}, {}, {}, {}, {}, {}, {}, {}
            ]
        }
        """.encode()
        forecast.status_code = 200

        with patch('requests.get', side_effect=[current, forecast]) as get:
            image = content.get_image((400, 300))

        get.assert_has_calls([
            call('https://api.openweathermap.org/data/2.5/weather?q=55901&units=imperial&appid=test'),
            call('https://api.openweathermap.org/data/2.5/forecast?q=55901&units=imperial&appid=test')
        ])

        # image.save(os.path.join(self.test_fixtures_dir, 'weather.png'), 'PNG')

        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))

    if __name__ == '__main__':
        unittest.main()
