from image_sources.image_source import ImageSource
from image_sources.image import ImageContent


class SlideshowContent(ImageSource):
    images = []
    image_index = 0
    interval = 10

    def get_configuration(self):
        return {
            'name': self.name,
            'images': {
                'type': 'textarea',
                'value': '\n'.join(map(lambda x: x.image_url, self.images))
            },
            'interval': self.interval
        }

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('images') is not None:
            self.images = []
            image_urls = params.get('images').split('\n')
            for image_url in image_urls:
                self.images.append(ImageContent({
                    'url': image_url
                }))
        if params.get('interval') is not None and params.get('interval') != '':
            self.interval = int(params.get('interval'))

    def get_image(self, size):
        if len(self.images) == 0:
            raise ValueError('No image URLs defined')

        image, _ = self.images[self.image_index].get_image(size)
        self.image_index = (self.image_index + 1) % len(self.images)

        return image, self.interval
