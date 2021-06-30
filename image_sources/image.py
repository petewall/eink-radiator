from enum import Enum, auto
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
import urllib.request
from PIL import Image, UnidentifiedImageError

from image_sources.image_source import ImageSource
from image_sources.blank import White


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
    image_error = None
    white_background = White()

    def get_configuration(self):
        return super().get_configuration() | {
            'url': self.image_url,
            'scale': {
                'type': 'select',
                'value': self.scale.name,
                'options': ImageScale.all_types()
            }
        }

    def set_image_url(self, url):
        self.image = None
        self.image_error = None
        self.image_url = url

        protocol = urlparse(url).scheme
        if protocol in ('http', 'https'):
            try:
                image_data = urllib.request.urlopen(self.image_url)
                self.image = Image.open(image_data)
            except HTTPError:
                self.image_error = 'Failed to fetch image'
            except UnidentifiedImageError:
                self.image_error = 'URL is not an image'
            except URLError:
                self.image_error = 'Bad URL'
        else:
            self.image_error = 'URL must use http(s)'


    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('scale') is not None:
            self.scale = ImageScale[params.get('scale')]
        if params.get('url') is not None:
            self.set_image_url(params.get('url'))

    def make_image(self, size):
        if self.image_url is None:
            raise ValueError('Image URL is required')

        if self.image is None:
            raise ValueError(self.image_error)

        if self.scale == ImageScale.scale:
            return self.image.resize(size), None

        if self.scale == ImageScale.contain:
            scaled = self.image.copy()
            scaled.thumbnail(size)
            image = self.image.resize(size)
            image.paste(self.white_background.get_image(size)[0])
            image.paste(scaled, box=(
                int((size[0] - scaled.size[0]) / 2),
                int((size[1] - scaled.size[1]) / 2)
            ))

            return image, None

        if self.scale == ImageScale.cover:
            scale_factor = max(
                size[0] / self.image.size[0],
                size[1] / self.image.size[1]
            )
            new_height = size[1] * scale_factor
            new_width = size[0] * scale_factor

            x_offset = int((self.image.size[0] - new_width) / 2)
            y_offset = int((self.image.size[1] - new_height) / 2)
            cropped = self.image.crop((
                x_offset,
                y_offset,
                x_offset + new_width,
                y_offset + new_height,
            ))
            return cropped.resize(size), None
        return None, None
