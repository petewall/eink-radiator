from routers.helpers import image_response
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse
from http import HTTPStatus
from screen import Screen
from slideshow import Slideshow
from image_sources.image_source import ImageSource

class ImageSourceRouter(APIRouter):
    def __init__(self, screen: Screen, slideshow: Slideshow):
        super().__init__()
        self.screen = screen
        self.slideshow = slideshow

        @self.get('/image_sources/{image_source_id}/configuration.json')
        def serve_image_source_configuration(request: Request, image_source_id: int = None):
            image_source = self.find_image_source_by_id(image_source_id)
            if image_source is None:
                return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

            return image_source.get_configuration()


        @self.get('/image_sources/{image_source_id}/image.png', response_class=StreamingResponse)
        def serve_image_source_image(request: Request, image_source_id: int = None):
            image_source = self.find_image_source_by_id(image_source_id)
            if image_source is None:
                return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

            return image_response(image_source.get_image(self.screen.size))

    def find_image_source_by_id(self, image_source_id: int) -> ImageSource:
        for image_source in self.slideshow.image_sources:
            if image_source.id == image_source_id:
                return image_source
        return None

