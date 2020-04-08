import unittest
from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock
from radiator import Radiator
from screen_fake import Screen


class FakeImageSource(object):
    image = "This is my image"

    def __init__(self):
        pass

    @classmethod
    def name(cls):
        return "Fake Image Source"

    def get_image(self):
        return self.image


class TestRadiator(TestCase):
    def test_refresh_sets_screen_image(self):
        radiator = Radiator([
            FakeImageSource()
        ])
        radiator.screen = MagicMock()
        radiator.refresh()

        radiator.screen.set_image.assert_called_once_with("This is my image")


if __name__ == '__main__':
    unittest.main()
