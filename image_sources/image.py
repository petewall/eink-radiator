from enum import Enum, auto
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
import urllib.request
from PIL import Image, UnidentifiedImageError
from color import Color
from image_sources.configuration import ConfigurationField, new_color_configuration_field, new_text_configuration_field
from image_sources.image_source import ImageSource


class ImageScale(Enum):
    SCALE = auto()
    CONTAIN = auto()
    COVER = auto()

    @classmethod
    def all_types(cls):
        return list(map(lambda x: x.name, list(cls)))


class ImageContent(ImageSource):
    def __init__(self, name: str = 'New Image Source', background_color: Color = Color.WHITE):
        super().__init__(name)
        self.configuration.data['scale'] = ConfigurationField(type='select', value=ImageScale.SCALE.name, options=ImageScale.all_types())
        self.configuration.data['url'] = new_text_configuration_field('url')
        self.configuration.data['background_color'] = new_color_configuration_field(background_color)

    def load_image(self):
        # TODO: load the raw image and cache.
        # Re-load only if the url changes
        # if only the scale or background changes, don't re-fetch the image

        url = self.configuration.data['url'].data
        if url is None:
            raise ValueError('Image URL is required')

        protocol = urlparse(url).scheme
        if protocol in ('http', 'https'):
            try:
                with urllib.request.urlopen(self.image_url) as image_data:
                    return Image.open(image_data)
            except HTTPError:
                raise ValueError('Failed to fetch image')
            except UnidentifiedImageError:
                raise ValueError('URL is not an image')
            except URLError:
                raise ValueError('Bad URL')
        else:
            raise ValueError(f'Unsupported protocol ({protocol})')

    async def make_image(self, size):
        image = self.load_image()

        scale = ImageScale(self.configuration.data['scale'].data)
        if scale == ImageScale.SCALE:
            return self.image.resize(size)

        if scale == ImageScale.CONTAIN:
            scaled = self.image.copy()
            scaled.thumbnail(size)
            image = self.image.resize(size)
            image.paste(self.white_background.get_image(size)[0])
            image.paste(scaled, box=(
                int((size[0] - scaled.size[0]) / 2),
                int((size[1] - scaled.size[1]) / 2)
            ))

            return image

        if scale == ImageScale.COVER:
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
            return cropped.resize(size)
        return None
