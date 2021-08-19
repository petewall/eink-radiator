# pylint: disable=no-self-use
import os
import unittest
from hamcrest import assert_that, equal_to, has_key, is_, not_
from PIL import Image
from color import Color
from image_sources.configuration import Configuration, new_color_configuration_field, new_text_configuration_field, new_textarea_configuration_field
from image_sources.text import TextContent
from pillow_image_matcher import the_same_image_as
from test_helpers import async_test


class TestTextContent(unittest.TestCase):
    test_fixtures_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures'
    )

    @async_test
    async def test_get_image(self):
        image_source = TextContent(
            TextContent.configuration(
                text='It is now safe to turn off your computer'
            )
        )
        image = await image_source.get_image((400, 300))

        if os.getenv('SAVE_TEST_FIXTURES') == 'true':
            image.save(os.path.join(self.test_fixtures_dir, 'text_1.png'))
        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'text_1.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

    @async_test
    async def test_image_with_different_background(self):
        image_source = TextContent(TextContent.configuration())
        changed = await image_source.set_configuration(Configuration(data={
            'name': new_text_configuration_field('Test Image'),
            'text': new_textarea_configuration_field('Shields up! Rrrrred alert!'),
            'foreground_color': new_color_configuration_field(Color.RED),
            'background_color': new_color_configuration_field(Color.BLACK),
            'superfluous': new_text_configuration_field('not relevant')
        }))
        assert_that(changed, is_(equal_to(True)))
        assert_that(image_source.configuration.data, not_(has_key('superfluous')))

        image = await image_source.get_image((400, 300))
        if os.getenv('SAVE_TEST_FIXTURES') == 'true':
            image.save(os.path.join(self.test_fixtures_dir, 'text_2.png'))

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'text_2.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

    @async_test
    async def test_multiline_string(self):
        image_source = TextContent(
            TextContent.configuration(
                text='Docker engineers\ndo it in a container',
                foreground_color=Color.WHITE,
                background_color=Color.BLACK
            )
        )

        image = await image_source.get_image((400, 300))
        if os.getenv('SAVE_TEST_FIXTURES') == 'true':
            image.save(os.path.join(self.test_fixtures_dir, 'text_3.png'))

        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'text_3.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()
