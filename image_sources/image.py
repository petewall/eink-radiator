from PIL import Image


class ImageContent():
    @classmethod
    def name(cls):
        return "Static Image"

    def __init__(self):
        self.image = Image.open("image_sources/InkywHAT-400x300.png")

    def get_image(self):
        return self.image
