# pylint: disable=import-error
from inky import InkyWHAT
from screen import Screen


class InkyScreen(Screen):
    def __init__(self):
        physical_screen = InkyWHAT('red')
        super().__init__((physical_screen.WIDTH, physical_screen.HEIGHT))
        self.screen = physical_screen

    def show_image(self):
        self.screen.set_image(self.image)
        self.screen.show()
