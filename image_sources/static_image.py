from PIL import Image
from image_sources.image_source import ImageSource


class StaticImageContent(ImageSource):
    image: Image = None

    async def make_image(self, _) -> Image:
        return self.image
