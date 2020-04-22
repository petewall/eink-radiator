import enum


class Color(enum.Enum):
    BLACK = 'black'
    WHITE = 'white'
    RED = 'red'

    @classmethod
    def all_colors(cls):
        return list(map(lambda x: x.value, list(cls)))
