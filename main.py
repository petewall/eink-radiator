#!/usr/bin/env python
import asyncio
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
slideshow.add_image_source(White())
slideshow.add_image_source(Black())
slideshow.add_image_source(Red())
slideshow.add_image_source(TextContent({"name": "Family", "text": "Pete\nBetsy\nGrace\nZach"}))

ui = UI(slideshow, screen)

async def main():
    port = os.environ.get('PORT', 5000)
    await asyncio.gather(
        slideshow.loop(),
        ui.start(port)
    )

if __name__ == '__main__':
    asyncio.run(main())