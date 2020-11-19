# pylint: disable=no-self-use
import os
from time import sleep
import unittest
from hamcrest import assert_that, calling, equal_to, has_entry, is_, less_than, raises
from PIL import Image
from image_sources.blank import Red, White
from image_sources.periodic_updating_image_source import PeriodicUpdatingImageSource
from pillow_image_matcher import the_same_image_as

class DummyImageSource(PeriodicUpdatingImageSource):
    image_sources = [
        Red(),
        White()
    ]
    index = 0
    def refresh_image(self, size):
        image, _ = self.image_sources[self.index].get_image(size)
        self.index += 1
        return image

class TestPeriodicUpdatingImageSource(unittest.TestCase):
    static_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'static'
    )

    def test_configuration_shows_interval(self):
        source = DummyImageSource({})
        config = source.get_configuration()
        assert_that(config, has_entry('interval', 60))

        source.set_configuration({
            'interval': 3600
        })
        _, interval = source.get_image((400, 300))
        assert_that(interval, is_(equal_to(3600)))

    def test_getting_the_image_returns_image_and_interval(self):
        source = DummyImageSource({
            'interval': 1234
        })
        image, interval = source.get_image((400, 300))
        expected_image = Image.open(os.path.join(self.static_dir, 'red.png'))
        assert_that(image, is_(the_same_image_as(expected_image)))
        expected_image.close()
        assert_that(interval, is_(equal_to(1234)))


    def test_getting_the_image_too_soon_returns_the_cached_image_and_remaining_interval(self):
        source = DummyImageSource({
            'interval': 1000
        })
        image1, interval = source.get_image((400, 300))
        assert_that(interval, is_(equal_to(1000)))
        sleep(0.5)

        image2, interval = source.get_image((400, 300))
        assert_that(interval, is_(less_than(1000)))

        assert_that(image1, is_(the_same_image_as(image2)))


    def test_setting_interval_too_short_gives_exceptions(self):
        source = DummyImageSource({
            'interval': 0
        })
        assert_that(calling(source.get_image).with_args((400, 300)), raises(ValueError))
