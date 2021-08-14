from image_sources.image_source import ImageSource
from typing import List
from color import Color
from image_sources.blank import BlankContent, White, Black, Red
from image_sources.configuration import Configuration
from image_sources.image import ImageContent, ImageScale
from image_sources.text import TextContent

class Persistence:
    def load(self) -> List[Configuration]:
        return [
            BlankContent.configuration(name='White', color=Color.WHITE),
            BlankContent.configuration(name='Black', color=Color.BLACK),
            BlankContent.configuration(name='Red', color=Color.RED),
            TextContent.configuration(name='Family', text='Pete\nBetsy\nGrace\nZach'),
            ImageContent.configuration(
                name='The Boys',
                url='https://thumbnails-photos.amazon.com/v1/thumbnail/O2Z2SysZTUOQrztKI65d7g?viewBox=1156%2C1540&ownerId=AQX0OIX0W30EP&groupShareToken=mCakTc1WSemv-NWcAh0ujw._PACKi8IHVck6agt8U1rxz',
                scale=ImageScale.CONTAIN,
                background_color=Color.BLACK
            )
        ]

    def save(configs: List[Configuration]):
        pass

    @classmethod
    def deserialize_image_source(cls, config: Configuration) -> ImageSource:
        if config.type == BlankContent.__name__:
            return BlankContent(config)
        elif config.type == ImageContent.__name__:
            return ImageContent(config)
        elif config.type == TextContent.__name__:
            return TextContent(config)
