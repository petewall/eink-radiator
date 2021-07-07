from PIL import Image
from image_sources.image_source import ImageSource


class StaticImageContent(ImageSource):
    image: Image = None

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('image_path'):
            self.image = Image.open(params.get('image_path'))

    def make_image(self, _) -> Image:
        return self.image
