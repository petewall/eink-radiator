# pylint: disable=no-self-use
import unittest
from hamcrest import assert_that, equal_to, is_, none
from image_sources.blank import Red
from image_sources.image_source import ImageSource

TEST_IMAGE = Red().make_image((400, 300))

class DummyImageSource(ImageSource):
    def make_image(self, size):
        assert_that(size, is_(equal_to((400, 300))))
        return TEST_IMAGE


class TestImageSource(unittest.TestCase):
    def test_configuration(self):
        content = DummyImageSource({})
        assert_that(content.name, is_(equal_to('New image source')))

        content.set_configuration({
            'name': 'new name'
        })
        assert_that(content.name, is_(equal_to('new name')))

    def test_get_image_returns_the_same(self):
        content = DummyImageSource({})
        assert_that(content.cached_image, is_(none()))

        image = content.get_image((400, 300))
        assert_that(image, is_(equal_to(TEST_IMAGE)))
        assert_that(content.cached_image, is_(equal_to(TEST_IMAGE)))

        image = content.get_image((400, 300))
        assert_that(image, is_(equal_to(TEST_IMAGE)))

    if __name__ == '__main__':
        unittest.main()
