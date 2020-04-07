import os
from image_sources.image import ImageContent
from image_sources.concourse.concourse import ConcourseContent
if os.environ.get('EINK_SCREEN_PRESENT'):
  from screen import Screen
else:
  from screen_fake import Screen

class Radiator:

  def __init__(self):
    self.image_sources = [
      ImageContent(),
      ConcourseContent()
    ]
    self.image_source = 1
    self.screen = Screen()
    self.refresh()

  def refresh(self):
    self.image = self.get_image_source().get_image()
    self.screen.set_image(self.image)
    self.screen.show()

  def get_image(self):
    return self.image

  def get_image_source(self):
    return self.image_sources[self.image_source]