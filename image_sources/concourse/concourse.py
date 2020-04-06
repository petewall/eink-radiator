from PIL import Image, ImageDraw, ImageFont

class ConcourseContent:
  """Build status from a concourse server"""

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
    image_canvas = ImageDraw.Draw(image)
    image_canvas.text((10, 10), 'Concourse', fill='white', font=self.title_font)
    return image
