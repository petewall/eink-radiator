import os
import unittest
from hamcrest import assert_that, has_entries, is_, none
from PIL import Image
from image_sources.blank import BlankContent
from pillow_image_matcher import the_same_image_as


class TestBlankContent(unittest.TestCase):
    test_fixtures_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures'
    )

    def test_get_image(self):
        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'blank_white.png'))

        content = BlankContent({})
        image, update_interval = content.get_image((400, 300))
        assert_that(update_interval, is_(none()))
        assert_that(image, is_(the_same_image_as(expected_image)))

        expected_image.close()

    def test_set_configuration(self):
        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'blank_red.png'))

        content = BlankContent({})
        content.set_configuration({
            'name': 'Red',
            'color': 'red',
            'superfluous': 'not relevant'
        })
        assert_that(content.get_configuration(), has_entries({
            'name': 'Red',
            'color': {
                'type': 'select',
                'value': 'red',
                'options': ['white', 'black', 'red']
            }
        }))

        image, update_interval = content.get_image((400, 300))
        assert_that(update_interval, is_(none()))
        assert_that(image, is_(the_same_image_as(expected_image)))

        expected_image.close()

    if __name__ == '__main__':
        unittest.main()
