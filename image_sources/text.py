# pylint: disable=method-hidden
import os
from transpose import Transpose
from PIL import Image, ImageDraw, ImageFont
from color import Color
from image_sources.configuration import Configuration, new_color_configuration_field, new_text_configuration_field, new_textarea_configuration_field, new_transform_configuration_field
from image_sources.image_source import ImageSource

FONT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'RobotoSlab-Regular.ttf')

async def make_error_image(message: str, size) -> Image:
    source = TextContent(TextContent.configuration(
        name='error message',
        text=message,
        foreground_color=Color.RED,
        background_color=Color.WHITE
    ))
    return await source.make_image(size)

class TextContent(ImageSource):
    font = ImageFont.truetype(font=FONT_PATH, size=30)

    @classmethod
    def configuration(cls, name: str = 'New Text Image Source', text: str = 'Lorem Ipsum', foreground_color: Color = Color.BLACK, background_color: Color = Color.WHITE, transform: Transpose = Transpose.NONE) -> Configuration:
        return Configuration(type=cls.__name__, data={
            'name': new_text_configuration_field(name),
            'text': new_textarea_configuration_field(text),
            'foreground_color': new_color_configuration_field(foreground_color),
            'background_color': new_color_configuration_field(background_color),
            'transform': new_transform_configuration_field(transform)
        })

    async def make_image(self, size) -> Image:
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

        transform = Transpose[self.configuration.data['transform'].value]
        return transform.apply(image)
