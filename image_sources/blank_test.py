import os
import unittest
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

        self.assertEqual(image.tobytes(), expected_image.tobytes())

    def test_set_configuration(self):
        expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'blank_red.png'))

        content = BlankContent({})
        content.set_configuration({
            'name': 'Red',
            'color': 'red',
            'superfluous': 'not relevant'
        })
        self.assertDictEqual(content.get_configuration(), {
            'name': 'Red',
            'color': {
                'value': 'red',
                'options': ['white', 'black', 'red']
            }
        })

        image = content.get_image((400, 300))
        self.assertEqual(image.tobytes(), expected_image.tobytes())

    if __name__ == '__main__':
        unittest.main()
