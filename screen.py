# pylint: disable=no-self-use
import time


class Screen:
    busy = False
    image = None

    def size(self):
        return 400, 300

    def set_image(self, image):
        if image != self.image:
            self.busy = True
            self.image = image.convert('P')
            self.show_image()
            self.busy = False

    def show_image(self):
        pass

    def get_image(self):
        while self.busy:
            time.sleep(0.5)
        return self.image
