# pylint: disable=global-statement
import os
from image_sources.image_source import ImageSource
from io import BytesIO
import logging
from http import HTTPStatus
from PIL import Image
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from screen import Screen
from slideshow import Slideshow, SlideshowObserver

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UI_INSTANCE = None

class UI(SlideshowObserver):
    def __init__(self, slideshow: Slideshow, screen: Screen):
        slideshow.add_subscriber(self)
        self.slideshow = slideshow
        self.screen = screen

    def update(self, slideshow: Slideshow) -> None:
        pass
  #   with slideshow.get_image_source() as image_source:
  #       self.set_image(image_source.get_image())

    def start(self, port: int) -> None:
        global UI_INSTANCE
        UI_INSTANCE = self
        logging.info('Starting UI on port %d\n', port)
        uvicorn.run('ui:app', host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', False))


@app.get('/', response_class=HTMLResponse)
async def serve_ui(request: Request):
    template_data = {
        'request': request,
        'height': UI_INSTANCE.screen.size[1],
        'width': UI_INSTANCE.screen.size[0],
        'slideshow': UI_INSTANCE.slideshow
    }
    return templates.TemplateResponse('index.html.jinja', template_data)

def find_image_source_by_id(image_source_id: int) -> ImageSource:
    for image_source in UI_INSTANCE.slideshow.image_sources:
        if image_source.id == image_source_id:
            return image_source
    return None


def image_response(image: Image):
    if image is None:
        return Response(status_code=HTTPStatus.NO_CONTENT)

    img_buffer = BytesIO()
    image.save(img_buffer, 'PNG')
    img_buffer.seek(0)
    response = StreamingResponse(img_buffer, media_type="image/png")
    response.headers['Cache-Control'] = 'no-cache'
    return response

@app.get('/image_sources/{image_source_id}/configuration.json')
async def serve_image_source_configuration(request: Request, image_source_id: int = None):
    image_source = find_image_source_by_id(image_source_id)
    if image_source is None:
        return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

    return image_source.get_configuration()


@app.get('/image_sources/{image_source_id}/image.png', response_class=StreamingResponse)
async def serve_image_source_image(request: Request, image_source_id: int = None):
    image_source = find_image_source_by_id(image_source_id)
    if image_source is None:
        return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

    return image_response(image_source.get_image(UI_INSTANCE.screen.size))

@app.route('/screen/image.png', methods=['GET'])
async def serve_screen_image(request: Request):
    return image_response(UI_INSTANCE.screen.image)
