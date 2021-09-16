import enum

from PIL import Image

class Transpose(enum.Enum):
    NONE = -1
    FLIP_LEFT_RIGHT = Image.FLIP_LEFT_RIGHT
    FLIP_TOP_BOTTOM = Image.FLIP_TOP_BOTTOM
    # ROTATE_90 = Image.ROTATE_90
    ROTATE_180 = Image.ROTATE_180
    # ROTATE_270 = Image.ROTATE_270
    # TRANSPOSE = Image.TRANSPOSE
    # TRANSVERSE = Image.TRANSVERSE

    @classmethod
    def all_methods(cls):
        return list(map(lambda x: x.name, list(cls)))

    def apply(self, image: Image) -> Image:
        if self == Transpose.NONE:
            return image

        return image.transpose(self.value)
