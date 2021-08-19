# pylint: disable=invalid-name,too-few-public-methods
from __future__ import annotations
from abc import abstractmethod, ABC
from copy import deepcopy
import logging
from typing import List
from PIL import Image
from image_sources.configuration import Configuration

class ImageSourceObserver(ABC):
    @abstractmethod
    async def image_source_update(self, image_source: ImageSource) -> None:
        pass

class ImageSource(ABC):
    def __init__(self, config: Configuration):
        self.id: int = id(self)
        self.logger = logging.getLogger(f'image_source_{self.id}')

        self.cached_image: Image = None
        self.configuration = config

        self.subscribers: List[ImageSourceObserver] = []

    def get_configuration(self) -> Configuration:
        return deepcopy(self.configuration)

    async def set_configuration(self, config: Configuration) -> bool:
        changed = self.configuration.update(config)
        if changed:
            self.logger.info('Configuration updated: %s', self.configuration.json())
            self.cached_image = None
            await self.notify()
        return changed

    def name(self) -> str:
        return self.configuration.data['name'].value

    def add_subscriber(self, subscriber: ImageSourceObserver) -> None:
        self.subscribers.append(subscriber)

    async def notify(self) -> None:
        for subscriber in self.subscribers:
            await subscriber.image_source_update(self)

    @abstractmethod
    async def make_image(self, size) -> Image:
        pass

    async def get_image(self, size, refresh: bool = False) -> Image:
        if refresh or self.cached_image is None or self.cached_image.size != size:
            self.cached_image = await self.make_image(size)
        return self.cached_image
