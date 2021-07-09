from __future__ import annotations
from abc import ABC, abstractmethod
import logging
import threading
import image_sources
from typing import List
from image_sources.image_source import ImageSource

# pylint: disable=too-few-public-methods
class SlideshowObserver(ABC):
    @abstractmethod
    def update(self, slideshow: Slideshow) -> None:
        pass

class Slideshow():
    index: int = 0
    image_sources: List[ImageSource] = []

    timer: threading.Timer = None
    interval: int = 5
    subscribers: List[SlideshowObserver] = []

    def __init__(self):
        self.notify()

    def start(self) -> None:
        self.timer = threading.Timer(self.interval, self.next)
        self.timer.start()

    def stop(self) -> None:
        self.timer.cancel()

    def next(self) -> None:
        self.index = (self.index + 1) % len(self.image_sources)
        logging.info(f'index is now {self.index}: {self.image_sources[self.index].name}')
        self.notify()
        self.start()

    def add_subscriber(self, subscriber: SlideshowObserver) -> None:
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: SlideshowObserver) -> None:
        self.subscribers.remove(subscriber)

    def notify(self) -> None:
        for subscriber in self.subscribers:
            subscriber.update(self)

    def add_image_source(self, image_source: ImageSource, index: int = -1) -> None:
        if index < 0:
            self.image_sources.append(image_source)
        else:
            self.image_sources.insert(index, image_source)

    def get_active_image_source(self) -> ImageSource:
        return self.image_sources[self.index]
