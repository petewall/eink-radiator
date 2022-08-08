import unittest
from hamcrest import assert_that, equal_to, is_
from color import Color

class TestColor(unittest.TestCase):
    def test_all_colors(self):
        colors = Color.all_colors()
        assert_that(colors, is_(equal_to(['WHITE', 'BLACK', 'RED'])))

    def test_palette(self):
        palette = Color.palette()
        assert_that(palette[0:3], is_(equal_to((255, 255, 255))))
        assert_that(palette[3:6], is_(equal_to((0, 0, 0))))
        assert_that(palette[6:9], is_(equal_to((255, 0, 0))))

if __name__ == '__main__':
    unittest.main()
