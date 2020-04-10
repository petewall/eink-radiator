from PIL import Image


class StaticImageContent:
    @classmethod
    def name(cls):
        return "Static Image"

    def __init__(self):
        self.image = Image.open("image_sources/static_image/InkywHAT-400x300.png")

    def get_image(self, _):
        return self.image
