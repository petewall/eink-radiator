import urllib.request
from PIL import Image
from image_sources.image_source import ImageSource


class ImageContent(ImageSource):
    image = None
    image_url = None

    def get_configuration(self):
        return {
            'name': self.name,
            'url': self.image_url
        }

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('url'):
            self.image_url = params.get('url')
            self.image = Image.open(urllib.request.urlopen(self.image_url))

    def get_image(self, size):
        if self.image is None:
            return None

        return self.image.resize(size)
