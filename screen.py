# pylint: disable=no-self-use,protected-access
import time
import threading
import traceback
from PIL import Image
from color import Color
from image_sources.text import TextContent


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
    'foreground_color': Color.red.name,
})


class Screen:
    busy = False
    image = None
    image_source = None
    image_size = None
    refresh_timer = None

    def __init__(self, size):
        self.image_size = size

    def size(self):
        return self.image_size

    def set_image_source(self, image_source):
        self.cancel_refresh_timer()
        self.image_source = image_source
        self.refresh()

    def generate_error_image(self, error_message):
        message = f'Failed to generate image:\n{error_message}'
        error_image.set_configuration({'text': message})
        return error_image.get_image(self.size())

    def cancel_refresh_timer(self):
        if self.refresh_timer is not None:
            self.refresh_timer.cancel()
            self.refresh_timer = None

    def refresh(self):
        if self.image_source is None:
            return

        refresh_interval = None
        try:
            image, refresh_interval = self.image_source.get_image(self.size())
        except BaseException as e:  # pylint: disable=broad-except
            traceback.print_exc()
            image, _ = self.generate_error_image(str(e))

        if refresh_interval is not None:
            self.refresh_timer = threading.Timer(refresh_interval, self.refresh)
            self.refresh_timer.start()
        self.set_image(image)

    def set_image(self, image):
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

    def get_image(self):
        while self.busy:
            time.sleep(0.5)
        return self.image
