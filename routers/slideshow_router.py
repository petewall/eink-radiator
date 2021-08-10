from http import HTTPStatus
from slideshow import Slideshow
from fastapi import APIRouter, Request
from fastapi.responses import Response

class SlideshowRouter(APIRouter):
    def __init__(self, slideshow: Slideshow):
        super().__init__()
        self.slideshow = slideshow

        @self.post('/slideshow/previous')
        async def previous_slide(request: Request):
            await self.slideshow.previous()
            return Response(status_code=HTTPStatus.OK)

        @self.post('/slideshow/next')
        async def next_slide(request: Request):
            await self.slideshow.next()
            return Response(status_code=HTTPStatus.OK)

        # @self.post('/slideshow/pause')
        # async def pause(request: Request):
        #     return image_response(self.screen.image)

        # @self.post('/slideshow/play')
        # async def play(request: Request):
        #     return image_response(self.screen.image)
