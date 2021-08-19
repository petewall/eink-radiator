#pylint: disable=no-self-use
import unittest
from PIL import Image
from hamcrest import assert_that, equal_to, is_, none
from image_sources.blank import Red
from image_sources.configuration import Configuration, new_text_configuration_field
from image_sources.image_source import ImageSource, ImageSourceObserver
from test_helpers import async_test

class DummyImageSource(ImageSource):
    test_image: Image = None

    def __init__(self):
        super().__init__(Configuration(data={
            'name': new_text_configuration_field('dummy image source')
        }))

    async def make_image(self, size):
        assert_that(size, is_(equal_to((400, 300))))
        return await Red().make_image((400, 300))


class TestImageSource(unittest.TestCase, ImageSourceObserver):
    image_source_updated: DummyImageSource = None
    def tearDown(self):
        self.image_source_updated = None

    @async_test
    async def test_get_image_returns_the_same(self):
        image_source = DummyImageSource()
        assert_that(image_source.cached_image, is_(none()))

        image = await image_source.get_image((400, 300))
        assert_that(image_source.cached_image, is_(equal_to(image)))

        image2 = await image_source.get_image((400, 300))
        assert_that(image, is_(equal_to(image2)))

    async def image_source_update(self, image_source: ImageSource) -> None:
        self.image_source_updated = image_source

    @async_test
    async def test_subscriptions(self):
        image_source = DummyImageSource()
        image_source.add_subscriber(self)

        assert_that(self.image_source_updated, is_(none()))
        config = image_source.get_configuration()
        config.data['name'].value = 'new name'
        await image_source.set_configuration(config)
        assert_that(self.image_source_updated, is_(image_source))
