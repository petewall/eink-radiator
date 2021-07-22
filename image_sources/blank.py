from image_sources.configuration import new_color_configuration_field
from PIL import Image
from image_sources.image_source import ImageSource
from color import Color


class BlankContent(ImageSource):
    def __init__(self, name: str, color: Color):
        super().__init__(name)
        self.configuration.data['color'] = new_color_configuration_field(color)

    def make_image(self, size) -> Image:
        color = Color[self.configuration.data['color'].value]
        image = Image.new('P', size, color.value)
        image.putpalette(Color.palette())
        return image


class White(BlankContent):
    def __init__(self):
        super().__init__('White', Color.WHITE)


class Black(BlankContent):
    def __init__(self):
        super().__init__('Black', Color.BLACK)


class Red(BlankContent):
    def __init__(self):
        super().__init__('Red', Color.RED)
