import os
from PIL import Image, ImageDraw, ImageFont
from image_sources.image_source import ImageSource
from color import Color

FONT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'RobotoSlab-Regular.ttf')


class TextContent(ImageSource):
    text = None
    foreground_color = Color.black
    background_color = Color.white
    font = ImageFont.truetype(font=FONT_PATH, size=30)

    def get_configuration(self):
        return {
            'name': self.name,
            'text': self.text,
            'foreground_color': {
                'value': self.foreground_color.name,
                'options': Color.all_colors()
            },
            'background_color': {
                'value': self.background_color.name,
                'options': Color.all_colors()
            },
        }

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('text'):
            self.text = params.get('text')
        if params.get('foreground_color'):
            self.foreground_color = Color[params.get('foreground_color')]
        if params.get('background_color'):
            self.background_color = Color[params.get('background_color')]

    def get_image(self, size):
        if self.text is None:
            return None

        image = Image.new('P', size, self.background_color.value)
        image.putpalette(Color.palette())
        image_canvas = ImageDraw.Draw(image)

        text_width, text_height = image_canvas.textsize(self.text, font=self.font)
        text_x = int((size[0] - text_width) / 2)
        text_y = int((size[1] - text_height) / 2)
        color = self.foreground_color.value
        image_canvas.text((text_x, text_y), self.text, fill=color, font=self.font)
        return image
