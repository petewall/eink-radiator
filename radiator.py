import os

if os.environ.get('EINK_SCREEN_PRESENT'):
    from screen import Screen
else:
    from screen_fake import Screen


class Radiator(object):
    image = None
    image_source = 0
    screen = Screen()

    def __init__(self, image_sources):
        self.image_sources = image_sources

    def refresh(self):
        self.image = self.get_image_source().get_image()
        self.screen.set_image(self.image)

    def get_image(self):
        return self.image

    def get_image_source(self):
        return self.image_sources[self.image_source]
