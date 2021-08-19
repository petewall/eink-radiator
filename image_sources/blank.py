# pylint: disable=method-hidden
from PIL import Image
from image_sources.configuration import Configuration, new_color_configuration_field, new_text_configuration_field
from image_sources.image_source import ImageSource
from color import Color


class BlankContent(ImageSource):
    @classmethod
    def configuration(cls, name: str, color: Color) -> Configuration:
        return Configuration(type=cls.__name__, data={
            'name': new_text_configuration_field(name),
            'color': new_color_configuration_field(color)
        })

    async def make_image(self, size) -> Image:
        color = Color[self.configuration.data['color'].value]
        image = Image.new('P', size, color.value)
        image.putpalette(Color.palette())
        return image


class White(BlankContent):
    def __init__(self):
        super().__init__(BlankContent.configuration('White', Color.WHITE))


class Black(BlankContent):
    def __init__(self):
        super().__init__(BlankContent.configuration('Black', Color.BLACK))


class Red(BlankContent):
    def __init__(self):
        super().__init__(BlankContent.configuration('Red', Color.RED))
