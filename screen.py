# pylint: disable=import-error
from inky import InkyWHAT


class Screen():
    def __init__(self):
        self.screen = InkyWHAT('red')

    def size(self):
        return (self.screen.WIDTH, self.screen.HEIGHT)

    def set_image(self, image):
        self.screen.set_image(image)
        self.screen.show()
