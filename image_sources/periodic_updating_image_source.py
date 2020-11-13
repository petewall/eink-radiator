from image_sources.image_source import ImageSource

class PeriodicUpdatingImageSource(ImageSource):
    interval = 10
    cached_image = None

    def get_configuration(self):
        return {
            'interval': self.interval
        }