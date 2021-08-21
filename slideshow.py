from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio
import logging
from typing import List
from image_sources.image_source import ImageSource, ImageSourceObserver

# pylint: disable=too-few-public-methods
class SlideshowObserver(ABC):
    @abstractmethod
    async def slideshow_update(self, slideshow: Slideshow) -> None:
        pass

class Slideshow(ImageSourceObserver):
    logger = logging.getLogger('slideshow')

    def __init__(self):
        self.index: int = 0
        self.image_sources: List[ImageSource] = []

        self.interval: int = 1 * 60  # ten minutes
        self.subscribers: List[SlideshowObserver] = []

        self.running = True
        self.sleep_handle: asyncio.Task = None

    async def loop(self) -> None:
        while self.running:
            self.sleep_handle = asyncio.create_task(asyncio.sleep(self.interval))
            try:
                await self.sleep_handle
                await self.next()
            except asyncio.CancelledError:
                pass
            self.sleep_handle = None

    async def next(self) -> None:
        self.index = (self.index + 1) % len(self.image_sources)
        await self.notify()
        self.reset()

    async def activate_slide(self, index: int) -> None:
        if index < 0 or index >= len(self.image_sources):
            return

        self.index = index
        await self.notify()
        self.reset()

    async def previous(self) -> None:
        self.index = self.index - 1
        if self.index < 0:
            self.index = len(self.image_sources) - 1
        await self.notify()
        self.reset()

    async def start(self) -> None:
        await self.notify()
        await self.loop()

    def stop(self) -> None:
        self.running = False
        self.reset()

    def reset(self) -> None:
        if self.sleep_handle is not None:
            self.sleep_handle.cancel()

    def add_subscriber(self, subscriber: SlideshowObserver) -> None:
        self.subscribers.append(subscriber)

    async def notify(self) -> None:
        self.logger.info('Slide #%d active: %s', self.index, self.image_sources[self.index].name())
        for subscriber in self.subscribers:
            await subscriber.slideshow_update(self)

    def add_image_source(self, image_source: ImageSource, index: int = -1) -> None:
        image_source.add_subscriber(self)
        if index < 0:
            self.image_sources.append(image_source)
        else:
            self.image_sources.insert(index, image_source)

    async def image_source_update(self, image_source: ImageSource) -> None:
        if self.get_active_image_source() == image_source:
            await self.notify()

    def get_active_image_source(self) -> ImageSource:
        return self.image_sources[self.index]
