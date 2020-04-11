from PIL import Image, ImageDraw, ImageFont
from image_sources.image_source import ImageSource

FONT_PATH = 'image_sources/concourse/RobotoSlab-Regular.ttf'


class ConcourseContent(ImageSource):
    url = None
    username = None
    password = None
    title_font = ImageFont.truetype(font=FONT_PATH, size=30)

    def get_configuration(self):
        return {
            'name': self.name,
            'url': self.url,
            'username': self.username,
            'password': self.password
        }

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('url'):
            self.url = params.get('url')
        if params.get('username'):
            self.username = params.get('username')
        if params.get('password'):
            self.password = params.get('password')

    def get_image(self, size):
        image = Image.new('RGB', size, 'black')

        logo = Image.open("image_sources/concourse/logo.png")
        image.paste(logo, box=(5, 5, 40, 40), mask=logo)

        image_canvas = ImageDraw.Draw(image)
        image_canvas.text((45, 3), 'Concourse', fill='white', font=self.title_font)
        image_canvas.line([(5, 47), (395, 47)], fill='red', width=2)
        return image
