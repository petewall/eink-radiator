from image_sources.text import make_error_image

from fastapi import APIRouter, Path, Query
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

        @self.post('/image_sources/{image_source_id}/activate')
        async def choose_slide(image_source_id: int = Path(..., title="The ID of the image source to activate", ge=0)):
            _, image_source = self.slideshow.find_image_source_by_id(image_source_id)
            if image_source is None:
                return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

            await self.slideshow.activate_slide(image_source)
            return Response(status_code=HTTPStatus.OK)

        @self.post('/image_sources/{image_source_id}/set_index')
        async def set_index(new_index: int, image_source_id: int = Path(..., title="The ID of the image source to re-order", ge=0)):
            index, image_source = self.slideshow.find_image_source_by_id(image_source_id)
            if image_source is None:
                return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

            if new_index == index:
                return Response(status_code=HTTPStatus.OK)

            await self.slideshow.set_image_source_index(image_source_id, new_index)
            return Response(status_code=HTTPStatus.OK)

        @self.get('/image_sources/{image_source_id}/configuration.json')
        async def serve_image_source_configuration(image_source_id: int = Path(..., title="The ID of the image source", ge=0)):
            _, image_source = self.slideshow.find_image_source_by_id(image_source_id)
            if image_source is None:
                return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

            return image_source.get_configuration().dict(exclude_unset=True)

        @self.post('/image_sources/{image_source_id}/configuration.json')
        async def update_image_source_configuration(image_source_id: int, configuration: Configuration):
            _, image_source = self.slideshow.find_image_source_by_id(image_source_id)
            if image_source is None:
                return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

            changed = await image_source.set_configuration(configuration)
            if changed:
                return image_source.get_configuration().dict(exclude_unset=True)
            else:
                return Response(status_code=HTTPStatus.NO_CONTENT)


        @self.get('/image_sources/{image_source_id}/image.png', response_class=StreamingResponse)
        async def serve_image_source_image(image_source_id: int = Path(..., title="The ID of the image source", ge=0)):
            _, image_source = self.slideshow.find_image_source_by_id(image_source_id)
            if image_source is None:
                return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

            try:
                image = await image_source.get_image(self.screen.size)
            except ValueError as e:
                image = await make_error_image(str(e), self.screen.size)
            return image_response(image)
