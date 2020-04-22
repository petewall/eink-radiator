# pylint: disable=import-error
from inky import InkyWHAT
from screen import Screen


class InkyScreen(Screen):
    def __init__(self):
        self.screen = InkyWHAT('red')

    def size(self):
        return self.screen.WIDTH, self.screen.HEIGHT

    def show_image(self):
        self.screen.set_image(self.image)
        self.screen.show()
