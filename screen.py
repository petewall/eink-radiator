from inky import inky, InkyWHAT


class Screen:
    """This displays an image on the InkyWhat"""

    def __init__(self):
        self.screen = InkyWHAT('red')

    def size(self):
        return (self.screen.WIDTH, self.screen.WIDTH)

    def set_image(self, image):
        self.screen.set_image(self.image)
        self.screen.show()
