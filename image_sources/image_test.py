# pylint: disable=no-self-use
import os
import unittest
from unittest.mock import patch
from hamcrest import assert_that, calling, equal_to, has_entries, is_, none, raises
from PIL import Image
from image_sources.image import ImageContent


@patch('urllib.request.urlopen')
class TestImageContent(unittest.TestCase):
    mock_image = None
    test_fixtures_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures'
    )

    def setUp(self):
        self.mock_image = open(os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'), 'rb')

    def tearDown(self):
        self.mock_image.close()

    def test_missing_url(self, urlopen):
        content = ImageContent({})
        assert_that(
            calling(content.get_image).with_args((1, 1)),
            raises(ValueError, "Image URL is required")
        )
        urlopen.assert_not_called()

    def test_get_image(self, urlopen):
        urlopen.return_value = self.mock_image

        content = ImageContent({
            'url': 'http://www.example.com/images/InkywHAT-400x300.png'
        })
        image, update_interval = content.get_image((400, 300))
        assert_that(update_interval, is_(none()))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image.png'))
        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))
        expected_image.close()

    def test_set_configuration(self, urlopen):
        urlopen.return_value = self.mock_image

        content = ImageContent({})
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

        image, update_interval = content.get_image((400, 300))
        assert_that(update_interval, is_(none()))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image.png'))
        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))
        expected_image.close()

    def test_scaled_image(self, urlopen):
        urlopen.return_value = self.mock_image

        content = ImageContent({
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'scale': 'scale'
        })
        image, update_interval = content.get_image((400, 300))
        assert_that(update_interval, is_(none()))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image_scaled.png'))
        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))
        expected_image.close()

    def test_contained_image(self, urlopen):
        urlopen.return_value = self.mock_image

        content = ImageContent({
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'scale': 'contain'
        })
        image, update_interval = content.get_image((400, 300))
        assert_that(update_interval, is_(none()))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image_contained.png'))
        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))
        expected_image.close()

    def test_covered_image(self, urlopen):
        urlopen.return_value = self.mock_image
        content = ImageContent({
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'scale': 'cover'
        })
        image, update_interval = content.get_image((400, 300))
        assert_that(update_interval, is_(none()))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image_covered.png'))
        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))
        expected_image.close()

    if __name__ == '__main__':
        unittest.main()
