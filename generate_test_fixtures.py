#!/usr/bin/env python

import os
from image_sources.blank import Red, White
from image_sources.image import ImageContent
from image_sources.text import TextContent
from unittest.mock import patch

def generate_text_1():
    content = TextContent({
        'text': 'It is now safe to turn off your computer'
    })
    image, _ = content.get_image((400, 300))
    image.save(os.path.join('test_fixtures', 'text_1.png'))

def generate_blank_red():
    content = Red()
    image, _ = content.get_image((400, 300))
    image.save(os.path.join('test_fixtures', 'blank_red.png'))

def generate_blank_white():
    content = White()
    image, _ = content.get_image((400, 300))
    image.save(os.path.join('test_fixtures', 'blank_white.png'))

def generate_image():
    source_image = open(os.path.join('test_fixtures', 'InkywHAT-400x300.png'), 'rb')
    with patch('urllib.request.urlopen', return_value=source_image):
        content = ImageContent({
            'url': 'http://www.example.com/images/InkywHAT-400x300.png',
            'scale': 'contain'
        })
        image, _ = content.get_image((200, 300))
        image.save(os.path.join('test_fixtures', 'image_contained_tall.png'))

        image, _ = content.get_image((400, 200))
        image.save(os.path.join('test_fixtures', 'image_contained_wide.png'))

        content.set_configuration({'scale': 'cover'})
        image, _ = content.get_image((200, 300))
        image.save(os.path.join('test_fixtures', 'image_covered_tall.png'))
        
        image, _ = content.get_image((400, 200))
        image.save(os.path.join('test_fixtures', 'image_covered_wide.png'))

        content.set_configuration({'scale': 'scale'})
        image, _ = content.get_image((200, 200))
        image.save(os.path.join('test_fixtures', 'image_scaled.png'))

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

def generate_weather():
    pass

generate_blank_red()
generate_blank_white()
generate_image()
generate_text_1()
generate_text_2()
generate_text_3()
generate_weather()