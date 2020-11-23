from PIL import Image
from image_sources.image_source import ImageSource
from color import Color


class BlankContent(ImageSource):
    color = Color.white

    def get_configuration(self):
        config = super().get_configuration()
        config.update({
            'color': {
                'type': 'select',
                'value': self.color.name,
                'options': Color.all_colors()
            }
        })
        return config

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
        super().__init__({'name': 'White', 'color': 'white'})


class Black(BlankContent):
    def __init__(self):
        super().__init__({'name': 'Black', 'color': 'black'})


class Red(BlankContent):
    def __init__(self):
        super().__init__({'name': 'Red', 'color': 'red'})
