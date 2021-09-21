from hamcrest.core.base_matcher import BaseMatcher

class PillowImageMatcher(BaseMatcher):
    def __init__(self, image):
        self.image = image

    def _matches(self, item):
        return self.image.tobytes() == item.tobytes()

    def describe_to(self, description):
        description.append_text(f'an image matching {self.image}')

def the_same_image_as(image):
    return PillowImageMatcher(image)
