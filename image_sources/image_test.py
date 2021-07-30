# pylint: disable=no-self-use
import os
from io import BytesIO
from urllib.error import HTTPError, URLError
import unittest
from unittest.mock import patch
from hamcrest import assert_that, calling, is_, raises
from PIL import Image
from image_sources.image import ImageContent, ImageScale
from pillow_image_matcher import the_same_image_as
from test_helpers import async_test


@patch('urllib.request.urlopen')
class TestImageContent(unittest.TestCase):
    mock_image = None
    test_fixtures_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures'
    )

    def setUp(self):
        # pylint: disable=consider-using-with
        self.mock_image_path = os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png')
        self.mock_image = open(self.mock_image_path, 'rb')

    def tearDown(self):
        self.mock_image.close()

    def test_load_image_missing_url(self, urlopen):
        image_source = ImageContent()
        assert_that(
            calling(image_source.load_image),
            raises(ValueError, "Image URL is required")
        )
        urlopen.assert_not_called()

    def test_load_image_only_http_and_https_protocols_are_allowed(self, _):
        image_source = ImageContent(
            name='image test',
            url='ftp://myserver.com/secret_image.png'
        )
        assert_that(
            calling(image_source.load_image),
            raises(ValueError, r'Unsupported protocol \(ftp\)')
        )

    def test_load_image_bad_urls_are_handled(self, urlopen):
        urlopen.side_effect = URLError('that url\'s bad, yo')
        image_source = ImageContent(
            name='image test',
            url='http://fk4248q#$%^'
        )
        assert_that(
            calling(image_source.load_image),
            raises(ValueError, r'Bad URL')
        )

    def test_load_image_bad_responses_are_handled(self, urlopen):
        urlopen.side_effect = HTTPError('https://this-always-500s', 500, 'told you', {}, None)
        image_source = ImageContent(
            name='image test',
            url='https://this-always-500s'
        )
        assert_that(
            calling(image_source.load_image),
            raises(ValueError, r'Failed to fetch image')
        )

    def test_load_image_responses_that_are_not_images_are_handled(self, urlopen):
        urlopen.return_value = BytesIO(b'this is not an image')
        image_source = ImageContent(
            name='image test',
            url='https://this-always-500s'
        )
        assert_that(
            calling(image_source.load_image),
            raises(ValueError, r'URL is not an image')
        )

    def test_load_image_from_file(self, urlopen):
        image_source = ImageContent(
            name='image test',
            url='file://' + self.mock_image_path
        )

        image = image_source.load_image()
        urlopen.assert_not_called()

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()


    def test_load_image(self, urlopen):
        urlopen.return_value = self.mock_image

        image_source = ImageContent(
            name='image test',
            url='http://www.example.com/images/InkywHAT-400x300.png'
        )

        image = image_source.load_image()
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

    @async_test
    async def test_get_image(self, urlopen):
        urlopen.return_value = self.mock_image

        image_source = ImageContent(
            name='image test',
            url='http://www.example.com/images/InkywHAT-400x300.png'
        )

        image = await image_source.get_image((400, 300))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

    @async_test
    async def test_scaled_image(self, urlopen):
        urlopen.return_value = self.mock_image

        image_source = ImageContent(
            name='image test',
            url='http://www.example.com/images/InkywHAT-400x300.png',
        )
        image = await image_source.get_image((200, 200))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image_scaled.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

        image = await image_source.get_image((400, 300))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

    @async_test
    async def test_contained_image(self, urlopen):
        urlopen.return_value = self.mock_image

        image_source = ImageContent(
            name='image test',
            url='http://www.example.com/images/InkywHAT-400x300.png',
            scale=ImageScale.CONTAIN
        )
        image = await image_source.get_image((400, 200))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(
            os.path.join(self.test_fixtures_dir, 'image_contained_wide.png')
        )
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

        image = await image_source.get_image((200, 300))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(
            os.path.join(self.test_fixtures_dir, 'image_contained_tall.png')
        )
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

        image = await image_source.get_image((400, 300))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

    @async_test
    async def test_covered_image(self, urlopen):
        urlopen.return_value = self.mock_image

        image_source = ImageContent(
            name='image test',
            url='http://www.example.com/images/InkywHAT-400x300.png',
            scale=ImageScale.COVER
        )
        image = await image_source.get_image((200, 300))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image_covered_tall.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

        image = await image_source.get_image((400, 200))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image_covered_wide.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

        image = await image_source.get_image((400, 300))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()
