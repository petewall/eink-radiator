# pylint: disable=no-self-use,protected-access
import time
from PIL import Image
from color import Color


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


class Screen:
    busy = False
    image = None

    def size(self):
        return 400, 300

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
