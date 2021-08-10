# pylint: disable=import-error
from inky import InkyWHAT
from screen import Screen


class InkyScreen(Screen):
    def __init__(self):
        physical_screen = InkyWHAT('red')
        super().__init__(physical_screen.resolution)
        self.hardware = physical_screen

    async def show_image(self):
        self.hardware.set_image(self.image)
        self.hardware.show()
