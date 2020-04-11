from PIL import Image
import urllib.request


class ImageContent:
    image = None
    url = None
    name = "Image"

    def __init__(self, params):
        if params is not None:
            self.set_configuration(params)

    def get_configuration(self):
        return {
            'name': self.name,
            'url': self.url
        }

    def set_configuration(self, params):
        if params.get('name'):
            self.name = params.get('name')
        if params.get('url'):
            self.url = params.get('url')
            self.image = Image.open(urllib.request.urlopen(self.url))

    def get_image(self, size):
        if self.image is not None:
            return self.image.resize(size)

