import os
from PIL import Image, ImageDraw, ImageFont
from image_sources.image_source import ImageSource

FONT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'RobotoSlab-Regular.ttf')


class TextContent(ImageSource):
    text = None
    font = ImageFont.truetype(font=FONT_PATH, size=30)

    def get_configuration(self):
        return {
            'name': self.name,
            'text': self.text
        }

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('text'):
            self.text = params.get('text')

    def get_image(self, size):
        image = Image.new('P', size, 'black')

        image_canvas = ImageDraw.Draw(image)
        text_width, text_height = image_canvas.textsize(self.text, font=self.font)
        text_x = int((size[0] - text_width) / 2)
        text_y = int((size[1] - text_height) / 2)
        image_canvas.text((text_x, text_y), self.text, fill='white', font=self.font)
        return image
