import os
import unittest
from hamcrest import assert_that, has_entries, is_
from PIL import Image
from color import Color
from image_sources.blank import BlankContent
from pillow_image_matcher import the_same_image_as


class TestBlankContent(unittest.TestCase):
    test_fixtures = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures'
    )

    def test_get_image(self):
        expected_image = Image.open(os.path.join(self.test_fixtures, 'white-400x300.png'))

        content = BlankContent(name='White', color=Color.WHITE)
        image = content.get_image((400, 300))
        assert_that(image, is_(the_same_image_as(expected_image)))

        expected_image.close()

    def test_set_configuration(self):
        expected_image = Image.open(os.path.join(self.test_fixtures, 'red-400x300.png'))

        content = BlankContent(name='Red', color=Color.RED)
        assert_that(content.get_configuration(), has_entries({
            'name': 'Red',
            'color': {
                'type': 'select',
                'value': 'red',
                'options': ['white', 'black', 'red']
            }
        }))

        image = content.get_image((400, 300))
        assert_that(image, is_(the_same_image_as(expected_image)))

        expected_image.close()

    if __name__ == '__main__':
        unittest.main()
