# pylint: disable=invalid-name
import json
import logging
from typing import List
from image_sources.blank import BlankContent
from image_sources.configuration import Configuration
from image_sources.image import ImageContent
from image_sources.image_source import ImageSource, ImageSourceObserver
from image_sources.text import TextContent
from slideshow import Slideshow, SlideshowObserver
from ui import UI

class PersistenceFile():
    def __init__(self, filename: str = 'data.json'):
        self.file = filename

    def load(self) -> List[Configuration]:
        with open(self.file, 'r') as file:
            raw_configs = json.load(file)
            image_source_configs = [Configuration.parse_obj(config) for config in raw_configs]
            return image_source_configs


    def save(self, image_source_configs: List[Configuration]):
        data = [config.dict() for config in image_source_configs]
        with open(self.file, 'w') as file:
            json.dump(obj=data, fp=file, indent=2)
            file.close()


class Persistence(ImageSourceObserver, SlideshowObserver):
    def __init__(self, slideshow: Slideshow, ui: UI):
        self.file = PersistenceFile()
        self.logger = logging.getLogger('persistence')
        self.slideshow = slideshow
        self.slideshow.add_subscriber(self)
        self.ui = ui

    def load(self) -> None:
        self.logger.info('Loading data from...')
        image_source_configs = self.file.load()

        for config in image_source_configs:
            image_source = self.deserialize_image_source(config)
            image_source.add_subscriber(self)
            image_source.add_subscriber(self.ui)
            self.slideshow.add_image_source(image_source)

    @classmethod
    def deserialize_image_source(cls, config: Configuration) -> ImageSource:
        if config.type == BlankContent.__name__:
            return BlankContent(config)
        if config.type == ImageContent.__name__:
            return ImageContent(config)
        if config.type == TextContent.__name__:
            return TextContent(config)
        raise TypeError(f'unknown image source type: {config.type}')

    def save(self) -> None:
        self.logger.info('Saving...')
        configs = [image_source.configuration for image_source in self.slideshow.image_sources]
        self.file.save(configs)

    async def image_source_update(self, image_source: ImageSource) -> None:
        self.save()

    async def slideshow_update(self, slideshow: Slideshow) -> None:
        pass # Do not need to update just because the active slide changed
    #     self.save()
