from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.hasmethod import hasmethod

class PillowImageMatcher(BaseMatcher):
    def __init__(self, image):
        self.image = image

    def _matches(self, other_image):
        return self.image.tobytes() == other_image.tobytes()

    def describe_to(self, description):
        description.append_text('an image matching {}'.format(self.image))

def the_same_image_as(image):
    return PillowImageMatcher(image)
