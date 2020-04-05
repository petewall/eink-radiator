from PIL import Image, ImageDraw

class ConcourseContent:
  """Build status from a concourse server"""

  @classmethod
  def name(cls):
    return "Concourse"

  # def __init__(self):
  #   self.image = Image.open("image_sources/InkywHAT-400x300.png")

  def get_image(self):
    image = Image.new('RGBA', (400, 300), 'black')
    image_canvas = ImageDraw.Draw(image)
    image_canvas.rectangle((70, 50, 270, 200), outline='red', fill='blue')
    image_canvas.text((70, 250), 'Hello World', fill='green')
    return image
