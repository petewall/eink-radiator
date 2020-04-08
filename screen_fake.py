class Screen:
    """This is a fake screen that shows the image in a window"""

    def size(self):
        return (400, 300)

    def set_image(self, image):
        image.show()
