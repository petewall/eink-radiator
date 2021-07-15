# pylint: disable=no-self-use,protected-access
from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio
import logging
from typing import List
from PIL import Image
from color import Color
from image_sources.text import TextContent
from slideshow import Slideshow, SlideshowObserver

def quantize(image, palette):
    """Convert an RGB or L mode image to use a given P image's palette."""
    # From https://stackoverflow.com/a/29438149/1255644

    image.load()
    palette.load()
    if palette.mode != 'P':
        raise ValueError('bad mode for palette image')
    if image.mode != 'RGB' and image.mode != 'L':
        raise ValueError('only RGB or L mode images can be quantized to a palette')
    converted_image = image.im.convert('P', 0, palette.im)  # the 0 means turn OFF dithering

    return image._new(converted_image)


error_image = TextContent({
    'name': 'Error Text',
    'foreground_color': Color.RED.name,
})

class ScreenObserver(ABC):
    @abstractmethod
    async def screen_update(self, screen: Screen) -> None:
        pass

class Screen(SlideshowObserver):
    busy = False
    image = None
    image_source = None
    image_size = None
    refresh_timer = None
    logger = None
    subscribers: List[ScreenObserver] = []

    def __init__(self, size, name="Screen"):
        self.size = size
        self.logger = logging.getLogger(name)

    def generate_error_image(self, error_message):
        message = f'Failed to generate image:\n{error_message}'
        error_image.set_configuration({'text': message})
        return error_image.get_image(self.size)

    def add_subscriber(self, subscriber: ScreenObserver) -> None:
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: ScreenObserver) -> None:
        self.subscribers.remove(subscriber)

    async def notify(self) -> None:
        for subscriber in self.subscribers:
            await subscriber.screen_update(self)

    async def slideshow_update(self, slideshow: Slideshow) -> None:
        image_source = slideshow.get_active_image_source()
        await self.set_image(image_source.get_image(self.size))

    async def set_image(self, image: Image):
        if image != self.image:
            self.busy = True
            await self.notify()

            if image.mode == 'RGBA':
                background = Image.new("RGB", image.size, 'white')
                background.paste(image, mask=image.split()[3])
                image = background

            if image.mode == 'RGB':
                palette = Image.new('P', (16, 16))
                palette.putpalette(Color.palette())
                image = quantize(image, palette)

            self.image = image
            self.show_image()
            await asyncio.sleep(1)
            self.busy = False
            await self.notify()

    def show_image(self):
        pass
