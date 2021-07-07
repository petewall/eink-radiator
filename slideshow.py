from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from image_sources.image_source import ImageSource

# pylint: disable=too-few-public-methods
class SlideshowObserver(ABC):
    @abstractmethod
    def update(self, slideshow: Slideshow) -> None:
        pass

class Slideshow():
    index = 3
    image_sources: List[ImageSource] = []

    # interval = 5*60
    subscribers: List[SlideshowObserver] = []

    def start(self) -> None:
        self.notify()

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
