from PIL import Image
from image_sources.image_source import ImageSource
from color import Color


class BlankContent(ImageSource):
    color = Color.white

    def get_configuration(self):
        return super().get_configuration() | {
            'color': {
                'type': 'select',
                'value': self.color.name,
                'options': Color.all_colors()
            }
        }

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('color'):
            self.color = Color[params.get('color')]

    def get_image(self, size):
        image = Image.new('P', size, self.color.value)
        image.putpalette(Color.palette())
        return image, None


class White(BlankContent):
    def __init__(self):
        super(White, self).__init__({'name': 'White', 'color': 'white'})


class Black(BlankContent):
    def __init__(self):
        super(Black, self).__init__({'name': 'Black', 'color': 'black'})


class Red(BlankContent):
    def __init__(self):
        super(Red, self).__init__({'name': 'Red', 'color': 'red'})
