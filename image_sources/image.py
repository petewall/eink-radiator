# pylint: disable=method-hidden
from enum import Enum, auto
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
import urllib.request
from PIL import Image, UnidentifiedImageError
from color import Color
from image_sources.blank import BlankContent
from image_sources.configuration import Configuration, ConfigurationField, new_color_configuration_field, new_text_configuration_field
from image_sources.image_source import ImageSource


class ImageScale(Enum):
    SCALE = auto()
    CONTAIN = auto()
    COVER = auto()

    @classmethod
    def all_types(cls):
        return list(map(lambda x: x.name, list(cls)))


def new_scale_configuration_field(value: ImageScale) -> ConfigurationField:
    return ConfigurationField(type='select', value=value.name, options=ImageScale.all_types())


class ImageContent(ImageSource):
    loaded_image_url: str = ''
    original_image: Image = None

    @classmethod
    def configuration(cls, name: str = 'New Image Source', url: str = '', scale: ImageScale = ImageScale.SCALE, background_color: Color = Color.WHITE):
        return Configuration(type=cls.__name__, data={
            'name': new_text_configuration_field(name),
            'scale': new_scale_configuration_field(scale),
            'url': new_text_configuration_field(url),
            'background_color': new_color_configuration_field(background_color),
        })

    async def set_configuration(self, config: Configuration) -> bool:
        changed = await super().set_configuration(config)
        if changed and self.configuration.data['url'].value != self.loaded_image_url:
            self.loaded_image_url = ''
        return changed

    def load_image(self) -> Image:
        url = self.configuration.data['url'].value
        if url is None or url == '':
            raise ValueError('Image URL is required')

        if url == self.loaded_image_url:
            return self.original_image

        parsed_url = urlparse(url)
        if parsed_url.scheme == 'file':
            self.original_image = Image.open(parsed_url.path)
            self.original_image.load()
            self.loaded_image_url = url
            return self.original_image
        if parsed_url.scheme in ('http', 'https'):
            try:
                with urllib.request.urlopen(url) as image_data:
                    self.original_image = Image.open(image_data)
                    self.original_image.load()
                    self.loaded_image_url = url
                    return self.original_image
            except HTTPError as http_error:
                raise ValueError('Failed to fetch image') from http_error
            except UnidentifiedImageError as unidentified_image_error:
                raise ValueError('URL is not an image') from unidentified_image_error
            except URLError as url_error:
                raise ValueError('Bad URL') from url_error
        else:
            raise ValueError(f'Unsupported protocol ({parsed_url.scheme})')

    async def make_background(self, size) -> Image:
        image_source = BlankContent(
            BlankContent.configuration(
                name='background',
                color=Color[self.configuration.data['background_color'].value]
            )
        )
        return await image_source.make_image(size)

    def make_scaled_image(self, size) -> Image:
        raw_image = self.load_image()
        return raw_image.resize(size)

    async def make_contained_image(self, size) -> Image:
        raw_image = self.load_image()

        scaled = raw_image.copy()
        scaled.thumbnail(size)
        image = raw_image.resize(size)
        image.paste(await self.make_background(size))
        image.paste(scaled, box=(
            int((size[0] - scaled.size[0]) / 2),
            int((size[1] - scaled.size[1]) / 2)
        ))

        return image

    def make_covered_image(self, size) -> Image:
        raw_image = self.load_image()
        scale_factor = max(
            size[0] / raw_image.size[0],
            size[1] / raw_image.size[1]
        )
        new_height = size[1] * scale_factor
        new_width = size[0] * scale_factor

        x_offset = int((raw_image.size[0] - new_width) / 2)
        y_offset = int((raw_image.size[1] - new_height) / 2)
        cropped = raw_image.crop((
            x_offset,
            y_offset,
            x_offset + new_width,
            y_offset + new_height,
        ))
        return cropped.resize(size)

    async def make_image(self, size) -> Image:
        scale = self.configuration.data['scale'].value
        if scale == ImageScale.SCALE.name:
            return self.make_scaled_image(size)
        if scale == ImageScale.CONTAIN.name:
            return await self.make_contained_image(size)
        if scale == ImageScale.COVER.name:
            return self.make_covered_image(size)
        return None
