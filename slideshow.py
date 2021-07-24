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
    index: int = -1  # Starting at -1 so the first time through the loop, it'll increment to 0
    image_sources: List[ImageSource] = []

    interval: int = 10 * 60  # ten minutes
    subscribers: List[SlideshowObserver] = []

    running = True
    sleep_handle: asyncio.Task = None 
    async def loop(self) -> None:
        while self.running:
            self.index = (self.index + 1) % len(self.image_sources)
            logging.info(f'index is now {self.index}: {self.image_sources[self.index].name}')
            await self.notify()

            self.sleep_handle = asyncio.create_task(asyncio.sleep(self.interval))
            try:
                await self.sleep_handle
            except asyncio.CancelledError:
                pass
            self.sleep_handle = None

    def stop(self) -> None:
        self.running = False
        if self.sleep_handle is not None:
            self.sleep_handle.cancel()

    def add_subscriber(self, subscriber: SlideshowObserver) -> None:
        self.subscribers.append(subscriber)

    async def notify(self) -> None:
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
            self.notify()

    def get_active_image_source(self) -> ImageSource:
        return self.image_sources[self.index]
