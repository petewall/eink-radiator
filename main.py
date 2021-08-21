#!/usr/bin/env python
import asyncio
import logging
import os
from persistence import Persistence
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
ui = UI(slideshow, screen)
persistence = Persistence(slideshow, ui)
persistence.load()

async def main():
    port = os.environ.get('PORT', 5000)
    await asyncio.gather(
        slideshow.start(),
        ui.start(port)
    )

if __name__ == '__main__':
    asyncio.run(main())
