import os
import unittest
from hamcrest import assert_that, equal_to, has_entries, is_, none
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
        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))

    def test_set_configuration(self):
        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'text_2.png'))

        content = TextContent({})
        image = content.get_image((400, 300))
        assert_that(image, is_(none()))

        content.set_configuration({
            'name': 'Test Image',
            'text': 'Shields up! Rrrrred alert!',
            'foreground_color': 'red',
            'background_color': 'black',
            'superfluous': 'not relevant'
        })
        assert_that(content.get_configuration(), has_entries({
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
        }))

        image = content.get_image((400, 300))
        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))

    def test_multiline_string(self):
        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'text_3.png'))

        content = TextContent({
            'text': 'Docker engineers\ndo it in a container',
            'foreground_color': 'white',
            'background_color': 'black'
        })
        assert_that(content.get_configuration(), has_entries({
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
        }))

        image = content.get_image((400, 300))

        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))
    if __name__ == '__main__':
        unittest.main()
