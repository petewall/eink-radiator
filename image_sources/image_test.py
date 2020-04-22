import os
import unittest
from unittest.mock import patch
from PIL import Image
from image_sources.image import ImageContent


@patch('urllib.request.urlopen')
class TestStaticImageContent(unittest.TestCase):
    mock_image = None
    expected_image = None
    test_fixtures_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures'
    )

    def setUp(self):
        self.expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'image.png'))
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
        self.assertEqual(image.tobytes(), self.expected_image.tobytes())

    def test_set_configuration(self, urlopen):
        urlopen.return_value = self.mock_image

        content = ImageContent({})
        image = content.get_image((400, 300))
        urlopen.assert_not_called()
        self.assertIsNone(image)

        content.set_configuration({
            'name': 'Test Image',
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'superfluous': 'not relevant'
        })
        self.assertEqual(content.get_configuration(), {
            'name': 'Test Image',
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
        })

        image = content.get_image((400, 300))
        urlopen.assert_called_with('http://www.example.com/images/InkywHAT-400x300.png')
        self.assertEqual(image.tobytes(), self.expected_image.tobytes())

    if __name__ == '__main__':
        unittest.main()
