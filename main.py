#!/usr/bin/env python
import asyncio
from typing import List
from image_sources.image_source import ImageSource
import logging
import os
from image_sources.text import TextContent
from image_sources.blank import White, Black, Red
from screen import Screen
from slideshow import Slideshow
from ui import UI

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

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
    TextContent('Family', 'Pete\nBetsy\nGrace\nZach')
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
