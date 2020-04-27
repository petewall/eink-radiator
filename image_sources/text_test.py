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
            'text': {
                'type': 'textarea',
                'value': 'Shields up! Rrrrred alert!'
            },
            'foreground_color': {
                'type': 'select',
                'value': 'red',
                'options': ['white', 'black', 'red']
            },
            'background_color': {
                'type': 'select',
                'value': 'black',
                'options': ['white', 'black', 'red']
            }
        })

        image = content.get_image((400, 300))
        self.assertEqual(image.tobytes(), expected_image.tobytes())

    def test_multiline_string(self):
        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'text_3.png'))

        content = TextContent({
            'text': 'Docker engineers\ndo it in a container',
            'foreground_color': 'white',
            'background_color': 'black'
        })
        self.assertDictEqual(content.get_configuration(), {
            'name': 'New image source',
            'text': {
                'type': 'textarea',
                'value': 'Docker engineers\ndo it in a container'
            },
            'foreground_color': {
                'type': 'select',
                'value': 'white',
                'options': ['white', 'black', 'red']
            },
            'background_color': {
                'type': 'select',
                'value': 'black',
                'options': ['white', 'black', 'red']
            }
        })

        image = content.get_image((400, 300))

        self.assertEqual(image.tobytes(), expected_image.tobytes())
    if __name__ == '__main__':
        unittest.main()
