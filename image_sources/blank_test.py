import os
import unittest
from hamcrest import assert_that, equal_to, is_
from PIL import Image
from color import Color
from image_sources.blank import White
from image_sources.configuration import Configuration, new_color_configuration_field
from pillow_image_matcher import the_same_image_as
from test_helpers import async_test


class TestBlankContent(unittest.TestCase):
    test_fixtures = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures'
    )

    @async_test
    async def test_get_image(self):
        image_source = White()
        image = await image_source.get_image((400, 300))

        expected_image = Image.open(os.path.join(self.test_fixtures, 'white-400x300.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()

    @async_test
    async def test_get_configuration(self):
        image_source = White()

        new_config = Configuration(data={
            'color': new_color_configuration_field(Color.RED)
        })
        changed = await image_source.set_configuration(new_config)
        assert_that(changed, is_(equal_to(True)))

        config = image_source.get_configuration()
        assert_that(config.data['name'].type, is_(equal_to('text')))
        assert_that(config.data['name'].value, is_(equal_to('White')))
        assert_that(config.data['color'].type, is_(equal_to('select')))
        assert_that(config.data['color'].value, is_(equal_to('RED')))
        assert_that(config.data['color'].options, is_(equal_to(Color.all_colors())))

        image = await image_source.get_image((400, 300))
        expected_image = Image.open(os.path.join(self.test_fixtures, 'red-400x300.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()
