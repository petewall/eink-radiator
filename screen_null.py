# pylint: disable=no-self-use


class Screen:
    image = None

    def size(self):
        return 400, 300

    def set_image(self, image):
        self.image = image.convert("P")

    def get_image(self):
        return self.image
