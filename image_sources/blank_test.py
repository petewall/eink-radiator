import os
import unittest
from hamcrest import assert_that, equal_to, has_entries, is_
from PIL import Image
from image_sources.blank import BlankContent


class TestTextContent(unittest.TestCase):
    test_fixtures_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures'
    )

    def test_get_image(self):
        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'blank_white.png'))

        content = BlankContent({})
        image = content.get_image((400, 300))

        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))

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

        image = content.get_image((400, 300))
        assert_that(image.tobytes(), is_(equal_to(expected_image.tobytes())))

    if __name__ == '__main__':
        unittest.main()
