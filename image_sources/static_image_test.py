import os
import unittest
from hamcrest import assert_that, equal_to, has_entries, is_, none
from PIL import Image
from image_sources.static_image import StaticImageContent


class TestStaticImageContent(unittest.TestCase):
    expected_image = None
    test_fixtures_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures'
    )

    def setUp(self):
        self.expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'static_image.png'))

    def test_get_image(self):
        content = StaticImageContent({
            'image_path': os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png')
        })
        image = content.get_image((400, 300))
        assert_that(image.tobytes(), is_(equal_to(self.expected_image.tobytes())))

    def test_set_configuration(self):
        content = StaticImageContent({})
        image = content.get_image((400, 300))
        assert_that(image, is_(none()))

        content.set_configuration({
            'name': 'Test Static Image',
            'image_path': os.path.join(self.test_fixtures_dir, 'InkywHAT-400x300.png'),
            'superfluous': 'not relevant'
        })
        assert_that(content.get_configuration(), has_entries({
            'name': 'Test Static Image'
        }))

        image = content.get_image((400, 300))
        assert_that(image.tobytes(), is_(equal_to(self.expected_image.tobytes())))

    if __name__ == '__main__':
        unittest.main()
