# pylint: disable=no-self-use
import os
import unittest
from hamcrest import assert_that, calling, has_entries, is_, raises
from PIL import Image
from image_sources.text import TextContent
from pillow_image_matcher import the_same_image_as


class TestTextContent(unittest.TestCase):
    test_fixtures_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures'
    )

    def test_missing_text(self):
        content = TextContent()
        assert_that(
            calling(content.get_image).with_args((1, 1)),
            raises(ValueError, "Text is required")
        )

    def test_get_image(self):
        content = TextContent({
            'text': 'It is now safe to turn off your computer'
        })
        image = content.get_image((400, 300))

        if os.getenv("SAVE_TEST_FIXTURES") == "true":
            image.save(os.path.join(self.test_fixtures_dir, 'text_1.png'))
        else:
            expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'text_1.png'))
            assert_that(image, is_(the_same_image_as(expected_image)))
            expected_image.close()

    def test_set_configuration(self):
        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'text_2.png'))

        content = TextContent({})
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
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

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
        assert_that(image, is_(the_same_image_as(expected_image)))
    if __name__ == '__main__':
        unittest.main()
