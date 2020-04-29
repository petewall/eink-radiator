import os
import unittest
from unittest.mock import patch
from hamcrest import assert_that, equal_to, has_entries, is_, none
from PIL import Image
from image_sources.image import ImageContent


@patch('urllib.request.urlopen')
class TestStaticImageContent(unittest.TestCase):
    mock_image = None
    test_fixtures_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures'
    )

    def setUp(self):
        self.mock_image = open(os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'), 'rb')

    def tearDown(self):
        self.mock_image.close()

    def test_get_image(self, urlopen):
        urlopen.return_value = self.mock_image

        content = ImageContent({
            'url': 'http://www.example.com/images/InkywHAT-400x300.png'
        })
        image = content.get_image((400, 300))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image.png'))
        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))

    def test_set_configuration(self, urlopen):
        urlopen.return_value = self.mock_image

        content = ImageContent({})
        image = content.get_image((400, 300))
        urlopen.assert_not_called()
        assert_that(image, is_(none()))

        content.set_configuration({
            'name': 'Test Image',
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'superfluous': 'not relevant'
        })
        assert_that(content.get_configuration(), has_entries({
            'name': 'Test Image',
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'scale': {
                'type': 'select',
                'value': 'scale',
                'options': ['scale', 'contain', 'cover']
            },
        }))

        image = content.get_image((400, 300))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image.png'))
        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))

    def test_scaled_image(self, urlopen):
        urlopen.return_value = self.mock_image

        content = ImageContent({
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'scale': 'scale'
        })
        image = content.get_image((200, 200))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image_scaled.png'))
        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))

    def test_contained_image(self, urlopen):
        urlopen.return_value = self.mock_image

        content = ImageContent({
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'scale': 'contain'
        })
        image = content.get_image((200, 200))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image_contained.png'))
        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))

    def test_covered_image(self, urlopen):
        urlopen.return_value = self.mock_image
        content = ImageContent({
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'scale': 'cover'
        })
        image = content.get_image((200, 200))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image_covered.png'))
        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))

    if __name__ == '__main__':
        unittest.main()
