# pylint: disable=import-error
from inky import InkyWHAT


class Screen:
    image = None

    def __init__(self):
        self.screen = InkyWHAT('red')

    def size(self):
        return self.screen.WIDTH, self.screen.HEIGHT

    def set_image(self, image):
        self.image = image.convert("P")
        self.screen.set_image(self.image)
        self.screen.show()

    def get_image(self):
        return self.image
