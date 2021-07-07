# pylint: disable=no-self-use,protected-access
import logging
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


class Screen(SlideshowObserver):
    busy = False
    image = None
    image_source = None
    image_size = None
    refresh_timer = None
    logger = None

    def __init__(self, size, name="Screen"):
        self.size = size
        self.logger = logging.getLogger(name)

    def generate_error_image(self, error_message):
        message = f'Failed to generate image:\n{error_message}'
        error_image.set_configuration({'text': message})
        return error_image.get_image(self.size)

    def update(self, slideshow: Slideshow) -> None:
        image_source = slideshow.get_active_image_source()
        self.set_image(image_source.get_image(self.size))

    def set_image(self, image: Image):
        if image != self.image:
            self.busy = True

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
            self.busy = False

    def show_image(self):
        pass
