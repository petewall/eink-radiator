# pylint: disable=no-self-use
import os
from io import BytesIO
from urllib.error import HTTPError, URLError
import unittest
from unittest.mock import patch
from hamcrest import assert_that, calling, has_entries, is_, none, raises
from PIL import Image
from image_sources.image import ImageContent
from pillow_image_matcher import the_same_image_as


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

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
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

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

    def test_scaled_image(self, urlopen):
        urlopen.return_value = self.mock_image

        content = ImageContent({
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'scale': 'scale'
        })
        image = content.get_image((200, 200))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image_scaled.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

        image = content.get_image((400, 300))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()


    def test_contained_image(self, urlopen):
        urlopen.return_value = self.mock_image

        content = ImageContent({
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'scale': 'contain'
        })
        image, update_interval = content.get_image((400, 200))
        assert_that(update_interval, is_(none()))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(
            os.path.join(self.test_fixtures_dir, 'image_contained_wide.png')
        )
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

        image, update_interval = content.get_image((200, 300))
        assert_that(update_interval, is_(none()))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(
            os.path.join(self.test_fixtures_dir, 'image_contained_tall.png')
        )
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

        image, update_interval = content.get_image((400, 300))
        assert_that(update_interval, is_(none()))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()


    def test_covered_image(self, urlopen):
        urlopen.return_value = self.mock_image
        content = ImageContent({
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'scale': 'cover'
        })
        image, update_interval = content.get_image((200, 300))
        assert_that(update_interval, is_(none()))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image_covered_tall.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

        image, update_interval = content.get_image((400, 200))
        assert_that(update_interval, is_(none()))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image_covered_wide.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

        image, update_interval = content.get_image((400, 300))
        assert_that(update_interval, is_(none()))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()


    def test_only_http_and_https_protocols_are_allowed(self, _):
        content = ImageContent({
            'url': 'file:///Users/pwall/Desktop/secret_image.png'
        })
        assert_that(
            calling(content.get_image).with_args((400, 300)),
            raises(ValueError, r'URL must use http\(s\)')
        )


    def test_bad_urls_are_handled(self, urlopen):
        urlopen.side_effect = URLError('that url\'s bad, yo')
        content = ImageContent({
            'url': 'http://fk4248q#$%^'
        })
        assert_that(
            calling(content.get_image).with_args((400, 300)),
            raises(ValueError, r'Bad URL')
        )


    def test_bad_responses_are_handled(self, urlopen):
        urlopen.side_effect = HTTPError('https://this-always-500s', 500, 'told you', {}, None)
        content = ImageContent({
            'url': 'https://this-always-500s'
        })
        assert_that(
            calling(content.get_image).with_args((400, 300)),
            raises(ValueError, r'Failed to fetch image')
        )


    def test_responses_that_are_not_images_are_handled(self, urlopen):
        urlopen.return_value = BytesIO(b'this is not an image')
        content = ImageContent({
            'url': 'https://this-always-500s'
        })
        assert_that(
            calling(content.get_image).with_args((400, 300)),
            raises(ValueError, r'URL is not an image')
        )


    if __name__ == '__main__':
        unittest.main()
