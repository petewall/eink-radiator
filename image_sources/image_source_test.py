#pylint: disable=no-self-use
import asyncio
import unittest
from PIL import Image
from hamcrest import assert_that, equal_to, is_, none
from image_sources.blank import Red
from image_sources.image_source import ImageSource

def async_test(coroutine):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coroutine(*args, **kwargs))
        finally:
            loop.close()
    return wrapper

class DummyImageSource(ImageSource):
    test_image: Image = None

    async def make_image(self, size):
        assert_that(size, is_(equal_to((400, 300))))
        return await Red().make_image((400, 300))


class TestImageSource(unittest.TestCase):
    def test_default_name(self):
        image_source = DummyImageSource()
        assert_that(image_source.name, is_(equal_to('New Image Source')))

    def test_configuration(self):
        image_source = DummyImageSource('test image source')
        assert_that(image_source.name, is_(equal_to('test image source')))

        config = image_source.configuration
        assert_that(config.data['id'].type, is_(equal_to('hidden')))
        assert_that(config.data['name'].type, is_(equal_to('text')))
        assert_that(config.data['name'].value, is_(equal_to('test image source')))

    @async_test
    async def test_get_image_returns_the_same(self):
        image_source = DummyImageSource()
        assert_that(image_source.cached_image, is_(none()))

        image = await image_source.get_image((400, 300))
        assert_that(image_source.cached_image, is_(equal_to(image)))

        image2 = await image_source.get_image((400, 300))
        assert_that(image, is_(equal_to(image2)))
