# pylint: disable=invalid-name,too-few-public-methods
from __future__ import annotations
from abc import abstractmethod, ABC
from typing import List
from image_sources import configuration
from image_sources.configuration import Configuration
from PIL import Image

class ImageSourceObserver(ABC):
    @abstractmethod
    async def image_source_update(self, image_source: ImageSource) -> None:
        pass

class ImageSource(ABC):
    id: int
    name: str

    cached_image = None
    configuration: Configuration
    subscribers: List[ImageSourceObserver] = []

    def __init__(self, name: str = 'New Image Source'):
        self.id = id(self)
        self.name = name

        self.configuration = Configuration()
        self.configuration.id = self.id
        self.configuration.name = self.name

    def get_configuration(self) -> Configuration:
        return self.configuration

    def set_configuration(self, config: Configuration) -> bool:
        return self.configuration.update(config)

    def add_subscriber(self, subscriber: ImageSourceObserver) -> None:
        self.subscribers.append(subscriber)

    async def notify(self) -> None:
        for subscriber in self.subscribers:
            await subscriber.image_source_update(self)

    @abstractmethod
    def make_image(self, size) -> Image:
        pass

    async def get_image(self, size, refresh: bool = False) -> Image:
        if refresh or self.cached_image is None or self.cached_image.size != size:
            self.cached_image = self.make_image(size)
            await self.notify()
        return self.cached_image
