# pylint: disable=no-self-use,protected-access
from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio
import logging
from time import sleep
from typing import List

from PIL import Image

from color import Color
from slideshow import Slideshow, SlideshowObserver

def quantize(image, palette):
    """Convert an RGB or L mode image to use a given P image's palette."""
    # From https://stackoverflow.com/a/29438149/1255644

    image.load()
    palette.load()
    if palette.mode != 'P':
        raise ValueError('bad mode for palette image')
    if image.mode not in ['RGB', 'L']:
        raise ValueError('only RGB or L mode images can be quantized to a palette')
    converted_image = image.im.convert('P', 0, palette.im)  # the 0 means turn OFF dithering

    return image._new(converted_image)


#pylint: disable=too-few-public-methods
class ScreenObserver(ABC):
    @abstractmethod
    async def screen_update(self, screen: Screen) -> None:
        pass


class Screen(SlideshowObserver):
    logger = logging.getLogger('screen')

    def __init__(self, size):
        self.busy = False
        self.image = None
        self.subscribers: List[ScreenObserver] = []
        self.size = size

    def add_subscriber(self, subscriber: ScreenObserver) -> None:
        self.subscribers.append(subscriber)

    async def notify(self) -> None:
        for subscriber in self.subscribers:
            await subscriber.screen_update(self)

    async def slideshow_update(self, slideshow: Slideshow, slide_changed=False, config_changed=False) -> None:
        if slide_changed:
            image_source = slideshow.get_active_image_source()
            new_image = await image_source.get_image(self.size)
            await self.set_image(new_image)

    async def set_image(self, image: Image):
        if image != self.image:
            self.busy = True
            await self.notify()

            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, 'white')
                background.paste(image, mask=image.split()[3])
                image = background

            if image.mode == 'RGB':
                palette = Image.new('P', (16, 16))
                palette.putpalette(Color.palette())
                image = quantize(image, palette)

            self.image = image

            self.logger.info('Setting new screen image')
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.show_image)
            self.logger.info('Finished setting new screen image')

            self.busy = False
            await self.notify()

    def show_image(self):
        sleep(1)
