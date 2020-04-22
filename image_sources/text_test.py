import os
import unittest
from PIL import Image
from image_sources.text import TextContent


class TestTextContent(unittest.TestCase):
    expected_image = None
    test_fixtures_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures'
    )

    def setUp(self):
        self.expected_image = Image.open(os.path.join(self.test_fixtures_dir, 'text.png'))

    def test_get_image(self):
        content = TextContent({
            'text': 'Shields up! Rrrrred alert!'
        })
        image = content.get_image((400, 300))
        self.assertEqual(image.tobytes(), self.expected_image.tobytes())

    def test_set_configuration(self):
        content = TextContent({})
        image = content.get_image((400, 300))
        self.assertIsNone(image)

        content.set_configuration({
            'name': 'Test Image',
            'text': 'Shields up! Rrrrred alert!',
            'superfluous': 'not relevant'
        })
        self.assertEqual(content.get_configuration(), {
            'name': 'Test Image',
            'text': 'Shields up! Rrrrred alert!'
        })

        image = content.get_image((400, 300))
        self.assertEqual(image.tobytes(), self.expected_image.tobytes())

    if __name__ == '__main__':
        unittest.main()
