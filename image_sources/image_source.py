from abc import abstractmethod, ABC
# pylint: disable=too-few-public-methods


class ImageSource(ABC):
    name = "New image source"

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
    def get_image(self, size):
        pass
