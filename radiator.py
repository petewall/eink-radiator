from image_sources.image import ImageContent
from image_sources.concourse import ConcourseContent

class Radiator:

  def __init__(self):
    self.image_sources = [
      ImageContent(),
      ConcourseContent()
    ]
    self.image_source = 1
    self.refresh()

  def refresh(self):
    self.image = self.get_image_source().get_image()

  def get_image(self):
    return self.image

  def get_image_source(self):
    return self.image_sources[self.image_source]