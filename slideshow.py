from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio
import logging
from typing import List
from image_sources.image_source import ImageSource

# pylint: disable=too-few-public-methods
class SlideshowObserver(ABC):
    @abstractmethod
    async def slideshow_update(self, slideshow: Slideshow) -> None:
        pass

class Slideshow():
    index: int = 0
    image_sources: List[ImageSource] = []

    interval: int = 5
    subscribers: List[SlideshowObserver] = []

    running = True
    sleep_handle: asyncio.Future = None 
    async def loop(self) -> None:
        while self.running:
            await self.notify()
            self.index = (self.index + 1) % len(self.image_sources)
            logging.info(f'index is now {self.index}: {self.image_sources[self.index].name}')
            self.sleep_handle = await asyncio.sleep(self.interval)

    def stop(self) -> None:
        self.running = False
        if self.sleep_handle is not None:
            self.sleep_handle.cancel()

    def add_subscriber(self, subscriber: SlideshowObserver) -> None:
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: SlideshowObserver) -> None:
        self.subscribers.remove(subscriber)

    async def notify(self) -> None:
        for subscriber in self.subscribers:
            await subscriber.slideshow_update(self)

    def add_image_source(self, image_source: ImageSource, index: int = -1) -> None:
        if index < 0:
            self.image_sources.append(image_source)
        else:
            self.image_sources.insert(index, image_source)

    def get_active_image_source(self) -> ImageSource:
        return self.image_sources[self.index]
