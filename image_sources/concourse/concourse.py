from PIL import Image, ImageDraw, ImageFont

FONT_PATH = 'image_sources/concourse/RobotoSlab-Regular.ttf'


class ConcourseContent:
    @classmethod
    def name(cls):
        return "Concourse"

    def __init__(self):
        self.url = None
        self.username = None
        self.password = None
        self.title_font = ImageFont.truetype(font=FONT_PATH, size=30)

    def get_image(self, size):
        image = Image.new('P', size, 'black')

        logo = Image.open("image_sources/concourse/logo.png")
        image.paste(logo, box=(5, 5, 40, 40), mask=logo)

        image_canvas = ImageDraw.Draw(image)
        image_canvas.text((45, 3), 'Concourse', fill='white', font=self.title_font)
        image_canvas.line([(5, 47), (395, 47)], fill='red', width=2)
        return image
