from PIL import Image


class StaticImageContent:
    name = "Static Image"

    def __init__(self, params):
        if params is not None:
            self.set_configuration(params)

    def get_configuration(self):
        return {
            'name': self.name
        }

    def set_configuration(self, params):
        if params.get('name'):
            self.name = params.get('name')

    def __init__(self, name=None):
        self.image = Image.open("image_sources/static_image/InkywHAT-400x300.png")
        if name is not None:
            self.name = name

    def get_image(self, _):
        return self.image
