# pylint: disable=invalid-name,too-few-public-methods
from abc import abstractmethod, ABC
from image_sources import configuration
from image_sources.configuration import Configuration
from PIL import Image

class ImageSource(ABC):
    id: int
    name: str

    cached_image = None
    configuration: Configuration

    def __init__(self, name: str = 'New Image Source'):
        self.id = id(self)
        self.name = name

        self.configuration = Configuration()
        self.configuration.id = self.id
        self.configuration.name = self.name

    def get_configuration(self) -> Configuration:
        return self.configuration

    def set_configuration(self, config: Configuration) -> bool:
        return self.configuration.update(config)

    @abstractmethod
    def make_image(self, size) -> Image:
        pass

    def get_image(self, size, refresh: bool = False) -> Image:
        if refresh or self.cached_image is None or self.cached_image.size != size:
            self.cached_image = self.make_image(size)
        return self.cached_image
