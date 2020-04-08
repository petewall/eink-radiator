from PIL import Image, ImageDraw, ImageFont


class ConcourseContent(object):
    @classmethod
    def name(cls):
        return "Concourse"

    def __init__(self):
        self.url = None
        self.username = None
        self.password = None
        self.title_font = ImageFont.truetype(font='image_sources/concourse/RobotoSlab-Regular.ttf', size=30)

    def get_image(self):
        image = Image.new('RGBA', (400, 300), 'black')

        logo = Image.open("image_sources/concourse/logo.png")
        image.paste(logo, box=(5, 5, 40, 40), mask=logo)

        image_canvas = ImageDraw.Draw(image)
        image_canvas.text((45, 3), 'Concourse', fill='white', font=self.title_font)
        image_canvas.line([(5, 47), (395, 47)], fill='red', width=2)
        return image
