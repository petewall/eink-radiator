# pylint: disable=too-few-public-methods


class ImageSource:
    name = "New image source"

    def __init__(self, params):
        if params is not None:
            self.set_configuration(params)

    def set_configuration(self, params):
        if params.get('name'):
            self.name = params.get('name')
