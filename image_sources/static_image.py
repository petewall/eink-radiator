from PIL import Image
from image_sources.image_source import ImageSource


class StaticImageContent(ImageSource):
    image = None

    def get_configuration(self):
        return {
            'name': self.name
        }

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('image_path'):
            self.image = Image.open(params.get('image_path'))

    def get_image(self, _):
        return self.image
