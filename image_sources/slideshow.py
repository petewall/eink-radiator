from image_sources.periodic_updating_image_source import PeriodicUpdatingImageSource
from image_sources.image import ImageContent


class SlideshowContent(PeriodicUpdatingImageSource):
    images = []
    image_index = 0

    def get_configuration(self):
        return super().get_configuration() | {
            'images': {
                'type': 'textarea',
                'value': '\n'.join(map(lambda x: x.image_url, self.images))
            }
        }

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('images') is not None:
            self.images = []
            image_urls = params.get('images').split('\n')
            for image_url in image_urls:
                if image_url != '':
                    self.images.append(ImageContent({
                        'url': image_url
                    }))

    def refresh_image(self, size):
        if len(self.images) == 0:
            raise ValueError('No image URLs defined')

        image, _ = self.images[self.image_index].get_image(size)
        self.image_index = (self.image_index + 1) % len(self.images)

        return image
