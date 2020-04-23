from enum import Enum, auto
import urllib.request
from PIL import Image

from color import Color
from image_sources.image_source import ImageSource


class ImageScale(Enum):
    scale = auto()
    contain = auto()
    cover = auto()

    @classmethod
    def all_types(cls):
        return list(map(lambda x: x.name, list(cls)))


class ImageContent(ImageSource):
    scale = ImageScale.scale
    image = None
    image_url = None

    def get_configuration(self):
        return {
            'name': self.name,
            'url': self.image_url,
            'scale': {
                'value': self.scale.name,
                'options': ImageScale.all_types()
            }
        }

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('scale'):
            self.scale = ImageScale[params.get('scale')]
        if params.get('url'):
            self.image_url = params.get('url')
            self.image = Image.open(urllib.request.urlopen(self.image_url))

    def get_image(self, size):
        if self.image is None:
            return None

        if self.scale == ImageScale.scale:
            return self.image.resize(size)

        if self.scale == ImageScale.contain:
            scaled = self.image.copy()
            scaled.thumbnail(size)
            image = Image.new(self.image.mode, size, Color.white.name)
            image.paste(scaled, box=(
                int((size[0] - scaled.size[0]) / 2),
                int((size[1] - scaled.size[1]) / 2)
            ))
            return image

        if self.scale == ImageScale.cover:
            size_ratio = size[0] / size[1]
            image_ratio = self.image.size[0] / self.image.size[1]
            image_is_wider = image_ratio > size_ratio
            image_is_taller = not image_is_wider
            new_width = self.image.size[1] * size_ratio if image_is_wider else self.image.size[0]
            new_height = self.image.size[0] * size_ratio if image_is_taller else self.image.size[1]
            x_offset = int((self.image.size[0] - new_width) / 2)
            y_offset = int((self.image.size[1] - new_height) / 2)
            cropped = self.image.crop((
                x_offset,
                y_offset,
                x_offset + new_width,
                y_offset + new_height,
            ))
            return cropped.resize(size)
        return None
