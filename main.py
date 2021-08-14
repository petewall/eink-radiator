#!/usr/bin/env python
import asyncio
import logging
import os
from persistence import Persistence
from screen import Screen
from slideshow import Slideshow
from ui import UI

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

persistence = Persistence()

if os.environ.get('EINK_SCREEN_PRESENT'):
    from inky_screen import InkyScreen
    screen = InkyScreen()
else:
    screen = Screen((400, 300))

slideshow = Slideshow()
slideshow.add_subscriber(screen)


ui = UI(slideshow, screen)

image_source_configurations = persistence.load()
for config in image_source_configurations:
    image_source = persistence.deserialize_image_source(config)
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
