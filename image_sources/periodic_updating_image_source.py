from abc import abstractmethod
import time
import threading
from image_sources.image_source import ImageSource

class PeriodicUpdatingImageSource(ImageSource):
    interval = 10
    next_refresh_time = 0
    cached_image = None
    lock = threading.Lock()

    def get_configuration(self):
        return super().get_configuration() | {
            'interval': self.interval
        }

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('interval') is not None and params.get('interval') != '':
            self.interval = int(params.get('interval'))
        self.next_refresh_time = 0

    def should_refresh_image(self):
        return self.cached_image is None or time.time() > self.next_refresh_time

    @abstractmethod
    def refresh_image(self, size):
        pass

    def get_image(self, size):
        if self.interval <= 0:
            raise ValueError('Interval must be greater than 0')

        self.lock.acquire()
        try:
            refresh_interval = self.interval
            if self.should_refresh_image():
                self.cached_image = self.refresh_image(size)
                self.next_refresh_time = time.time() + self.interval
            else:
                refresh_interval = self.next_refresh_time - time.time()
        finally:
            self.lock.release()

        return self.cached_image, refresh_interval
