from inky import inky, InkyWHAT

class Screen:
  """This is a fake screen that shows the image in a window"""

  def __init__(self):
    self.image = None
    self.screen = InkyWHAT('red')

  def size(self):
    return (self.screen.WIDTH, self.screen.WIDTH)

  def get_image(self):
    return self.image

  def set_image(self, image):
    self.image = image

  def show(self):
    if self.image is not None:
      self.screen.set_image(self.image)
      self.screen.show()
