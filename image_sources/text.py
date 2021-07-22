from image_sources.configuration import new_color_configuration_field, new_textarea_configuration_field
import os
from PIL import Image, ImageDraw, ImageFont
from image_sources.image_source import ImageSource
from color import Color

FONT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'RobotoSlab-Regular.ttf')


class TextContent(ImageSource):
    font = ImageFont.truetype(font=FONT_PATH, size=30)

    def __init__(self, name: str = 'New Text Image Source', text: str = 'Lorem Ipsum', foreground_color: Color = Color.BLACK, background_color: Color = Color.WHITE):
        super().__init__(name)
        self.configuration.data['text'] = new_textarea_configuration_field(text)
        self.configuration.data['foreground_color'] = new_color_configuration_field(foreground_color)
        self.configuration.data['background_color'] = new_color_configuration_field(background_color)

    def make_image(self, size) -> Image:
        text = self.configuration.data['text'].value
        if text is None:
            raise ValueError('Text is required')

        color = Color[self.configuration.data['background_color'].value].value
        image = Image.new('P', size, color)
        image.putpalette(Color.palette())
        image_canvas = ImageDraw.Draw(image)

        text_width, text_height = image_canvas.textsize(text, font=self.font)
        text_x = int((size[0] - text_width) / 2)
        text_y = int((size[1] - text_height) / 2)
        color = Color[self.configuration.data['foreground_color'].value].value
        image_canvas.text((text_x, text_y), text, fill=color, font=self.font, align='center')
        return image
