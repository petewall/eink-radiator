class Screen:
  """This is a fake screen that shows the image in a window"""

  def __init__(self):
    self.image = None

  def size(self):
    return (400, 300)

  def get_image(self):
    return self.image

  def set_image(self, image):
    self.image = image

  def show(self):
    if self.image is not None:
      self.image.show()
