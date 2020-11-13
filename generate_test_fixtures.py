#!/usr/bin/env python

import os
from image_sources.text import TextContent

def generate_text_1():
    content = TextContent({
        'text': 'It is now safe to turn off your computer'
    })
    image, _ = content.get_image((400, 300))
    image.save(os.path.join('test_fixtures', 'text_1.png'))

def generate_text_2():
    content = TextContent({
        'name': 'Test Image',
        'text': 'Shields up! Rrrrred alert!',
        'foreground_color': 'red',
        'background_color': 'black',
        'superfluous': 'not relevant'
    })
    image, _ = content.get_image((400, 300))
    image.save(os.path.join('test_fixtures', 'text_2.png'))

def generate_text_3():
    content = TextContent({
        'text': 'Docker engineers\ndo it in a container',
        'foreground_color': 'white',
        'background_color': 'black'
    })
    image, _ = content.get_image((400, 300))
    image.save(os.path.join('test_fixtures', 'text_3.png'))

generate_text_1()
generate_text_2()
generate_text_3()