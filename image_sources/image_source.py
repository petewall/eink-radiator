from abc import abstractmethod, ABC
# pylint: disable=too-few-public-methods

class ImageSource(ABC):
    name = "New image source"
    cached_image = None

    def __init__(self, params):
        if params is not None:
            self.set_configuration(params)

    def get_configuration(self):
        return {
            'name': self.name,
        }

    def set_configuration(self, params):
        if params.get('name'):
            self.name = params.get('name')

    @abstractmethod
    def make_image(self, size):
        pass

    def get_image(self, size):
        if self.cached_image is None or self.cached_image.size != size:
            self.cached_image = self.make_image(size)
        return self.cached_image
