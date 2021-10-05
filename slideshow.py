from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio
from copy import deepcopy
from datetime import datetime
import logging
from typing import List, Set, Tuple

from image_sources.configuration import Configuration, new_number_configuration_field
from image_sources.image_source import ImageSource, ImageSourceObserver

# pylint: disable=too-few-public-methods
class SlideshowObserver(ABC):
    @abstractmethod
    async def slideshow_update(self, slideshow: Slideshow, slide_activated=False, slideshow_changed=False, config_changed=False) -> None:
        pass

DEFAULT_INTERVAL = 10*60

# pylint: disable=too-many-instance-attributes
class Slideshow(ImageSourceObserver):
    logger = logging.getLogger('slideshow')

    def __init__(self):
        self.configuration = Configuration(type=Slideshow.__name__, data={
            'interval': new_number_configuration_field(DEFAULT_INTERVAL)
        })

        self.active_image_source: ImageSource = None
        self.image_sources: List[ImageSource] = []

        self.current_slide_start_time = datetime.now()
        self.current_interval = int(self.configuration.get('interval'))
        self.subscribers: Set[SlideshowObserver] = []

        self.running = True
        self.sleep_handle: asyncio.Task = None

    async def loop(self) -> None:
        while self.running:
            self.current_slide_start_time = datetime.now()
            self.current_interval = int(self.configuration.get('interval'))
            self.sleep_handle = asyncio.create_task(asyncio.sleep(self.current_interval))
            try:
                await self.sleep_handle
                await self.next()
            except asyncio.CancelledError:
                pass
            self.sleep_handle = None

    async def next(self) -> None:
        use_next = False
        for _, image_source in enumerate(self.image_sources):
            if use_next:
                await self.activate_slide(image_source)
                return
            if image_source == self.active_image_source:
                use_next = True
        if use_next:
            await self.activate_slide(self.image_sources[0])

    async def activate_slide(self, image_source: ImageSource) -> None:
        if self.active_image_source == image_source:
            return
        self.active_image_source = image_source
        await self.notify(slide_activated=True)
        self.reset()

    async def previous(self) -> None:
        previous = self.image_sources[len(self.image_sources) - 1]
        for _, image_source in enumerate(self.image_sources):
            if image_source == self.active_image_source:
                await self.activate_slide(previous)
                return
            previous = image_source

    async def start(self) -> None:
        await self.activate_slide(self.image_sources[0])
        await self.loop()

    def stop(self) -> None:
        self.running = False
        self.reset()

    def reset(self) -> None:
        if self.sleep_handle is not None:
            self.sleep_handle.cancel()

    def second_elapsed(self):
        return (datetime.now() - self.current_slide_start_time).total_seconds()

    def seconds_remaining(self):
        return self.current_interval - self.second_elapsed()

    def get_configuration(self) -> Configuration:
        return deepcopy(self.configuration)

    async def set_configuration(self, config: Configuration) -> bool:
        changed = self.configuration.update(config)
        if changed:
            self.logger.info('Configuration updated: %s', self.configuration.json())
        await self.notify(config_changed=True)
        return changed

    def add_subscriber(self, subscriber: SlideshowObserver) -> None:
        self.subscribers.append(subscriber)

    async def notify(self, slide_activated=False, slideshow_changed=False, config_changed=False) -> None:
        if slide_activated:
            self.logger.info('Slide active: %s', self.active_image_source.name())
        for subscriber in self.subscribers:
            await subscriber.slideshow_update(self, slide_activated, slideshow_changed, config_changed)

    def add_image_source(self, image_source: ImageSource, index: int = -1) -> None:
        image_source.add_subscriber(self)
        if index < 0:
            self.image_sources.append(image_source)
        else:
            self.image_sources.insert(index, image_source)

    async def image_source_update(self, image_source: ImageSource) -> None:
        if self.active_image_source == image_source:
            await self.notify(slide_activated=True)

    async def set_image_source_index(self, image_source_id: int, new_index: int) -> None:
        index, image_source = self.find_image_source_by_id(image_source_id)
        self.logger.info('Image source %d moving from #%d to #%d', image_source.id, index, new_index)
        if index == new_index:
            return
        self.image_sources.pop(index)
        self.add_image_source(image_source, new_index)
        await self.notify(slideshow_changed=True)

    def find_image_source_by_id(self, image_source_id: int) -> Tuple[int, ImageSource]:
        for index, image_source in enumerate(self.image_sources):
            if image_source.id == image_source_id:
                return index, image_source
        return None, None
