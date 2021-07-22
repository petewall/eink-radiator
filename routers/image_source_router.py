from typing import Dict

from fastapi import APIRouter
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse
from http import HTTPStatus
from screen import Screen
from slideshow import Slideshow
from image_sources.configuration import Configuration
from image_sources.image_source import ImageSource
from routers.helpers import image_response

class ImageSourceRouter(APIRouter):
    def __init__(self, screen: Screen, slideshow: Slideshow):
        super().__init__()
        self.screen = screen
        self.slideshow = slideshow

        @self.get('/image_sources/{image_source_id}/configuration.json')
        def serve_image_source_configuration(image_source_id: int):
            image_source = self.find_image_source_by_id(image_source_id)
            if image_source is None:
                return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

            return image_source.get_configuration()

        @self.post('/image_sources/{image_source_id}/configuration.json')
        def update_image_source_configuration(image_source_id: int, configuration: Configuration):
            image_source = self.find_image_source_by_id(image_source_id)
            if image_source is None:
                return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

            changed = image_source.set_configuration(configuration)
            if changed:
                image_source.get_image(self.screen.size, refresh=True)
                return Response(status_code=HTTPStatus.OK)
            else:
                return Response(status_code=HTTPStatus.NO_CONTENT)


        @self.get('/image_sources/{image_source_id}/image.png', response_class=StreamingResponse)
        def serve_image_source_image(image_source_id: int = None):
            image_source = self.find_image_source_by_id(image_source_id)
            if image_source is None:
                return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

            return image_response(image_source.get_image(self.screen.size))

    def find_image_source_by_id(self, image_source_id: int) -> ImageSource:
        for image_source in self.slideshow.image_sources:
            if image_source.id == image_source_id:
                return image_source
        return None

