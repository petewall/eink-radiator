import enum


class Color(enum.Enum):
    WHITE = 0
    BLACK = 1
    RED = 2

    @classmethod
    def all_colors(cls):
        return list(map(lambda x: x.name, list(cls)))

    @classmethod
    def palette(cls):
        return (255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252
