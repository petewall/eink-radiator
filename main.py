#!/usr/bin/env python
import asyncio
import logging
import os
from typing import List
from color import Color
from image_sources.blank import White, Black, Red
from image_sources.image import ImageContent, ImageScale
from image_sources.image_source import ImageSource
from image_sources.text import TextContent
from screen import Screen
from slideshow import Slideshow
from ui import UI

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if os.environ.get('EINK_SCREEN_PRESENT'):
    from inky_screen import InkyScreen
    screen = InkyScreen()
else:
    screen = Screen((400, 300))

slideshow = Slideshow()
slideshow.add_subscriber(screen)

image_sources: List[ImageSource] = [
    White(),
    Black(),
    Red(),
    TextContent('Family', 'Pete\nBetsy\nGrace\nZach'),
    ImageContent(
        name='The Boys',
        url='https://thumbnails-photos.amazon.com/v1/thumbnail/O2Z2SysZTUOQrztKI65d7g?viewBox=1156%2C1540&ownerId=AQX0OIX0W30EP&groupShareToken=mCakTc1WSemv-NWcAh0ujw._PACKi8IHVck6agt8U1rxz',
        scale=ImageScale.CONTAIN,
        background_color=Color.BLACK
    )
]
ui = UI(slideshow, screen)

for image_source in image_sources:
    slideshow.add_image_source(image_source)
    image_source.add_subscriber(ui)

async def main():
    port = os.environ.get('PORT', 5000)
    await asyncio.gather(
        slideshow.loop(),
        ui.start(port)
    )

if __name__ == '__main__':
    asyncio.run(main())
