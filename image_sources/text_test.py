import os
import unittest
from PIL import Image
from image_sources.text import TextContent


class TestTextContent(unittest.TestCase):
    test_fixtures_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures'
    )

    def test_get_image(self):
        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'text_1.png'))

        content = TextContent({
            'text': 'It is now safe to turn off your computer'
        })
        image = content.get_image((400, 300))
        self.assertEqual(image.tobytes(), expected_image.tobytes())

    def test_set_configuration(self):
        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'text_2.png'))

        content = TextContent({})
        image = content.get_image((400, 300))
        self.assertIsNone(image)

        content.set_configuration({
            'name': 'Test Image',
            'text': 'Shields up! Rrrrred alert!',
            'foreground_color': 'red',
            'background_color': 'black',
            'superfluous': 'not relevant'
        })
        self.assertDictEqual(content.get_configuration(), {
            'name': 'Test Image',
            'text': 'Shields up! Rrrrred alert!',
            'foreground_color': {
                'value': 'red',
                'options': ['black', 'white', 'red']
            },
            'background_color': {
                'value': 'black',
                'options': ['black', 'white', 'red']
            }
        })

        image = content.get_image((400, 300))
        self.assertEqual(image.tobytes(), expected_image.tobytes())

    if __name__ == '__main__':
        unittest.main()
