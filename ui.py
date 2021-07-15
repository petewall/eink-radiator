# pylint: disable=global-statement
import asyncio
from typing import Any, List

from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocketState
from image_sources.image_source import ImageSource
from io import BytesIO
import logging
from http import HTTPStatus
from PIL import Image
from fastapi import FastAPI, HTTPException, Request, WebSocket
from fastapi.responses import HTMLResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from screen import Screen
from slideshow import Slideshow, SlideshowObserver

def image_response(image: Image):
    if image is None:
        return Response(status_code=HTTPStatus.NO_CONTENT)

    img_buffer = BytesIO()
    image.save(img_buffer, 'PNG')
    img_buffer.seek(0)
    response = StreamingResponse(img_buffer, media_type="image/png")
    response.headers['Cache-Control'] = 'no-cache'
    return response

USERS: List[WebSocket] = []

class UI(FastAPI, SlideshowObserver):
    # users: List[WebSocket] = []
    templates = Jinja2Templates(directory='templates')

    def __init__(self, slideshow: Slideshow, screen: Screen):
        super().__init__(title="eInkRadiatorUI")

        self.mount("/static", StaticFiles(directory="static"), name="static")

        self.screen = screen
        self.slideshow = slideshow
        self.slideshow.add_subscriber(self)

        # class UserListMiddleware:
        #     def __init__(self, app: UI):
        #         self._app = app
        #         self._users = app.users

        #     async def __call__(self, scope: Scope, receive: Receive, send: Send):
        #         if scope["type"] in ("lifespan", "http", "websocket"):
        #             scope["users"] = self._users
        #         await self._app(scope, receive, send)

        # self.add_middleware(UserListMiddleware)


        @self.get('/', response_class=HTMLResponse)
        def serve_ui(request: Request):
            template_data = {
                'request': request,
                'height': self.screen.size[1],
                'width': self.screen.size[0],
                'slideshow': self.slideshow
            }
            return self.templates.TemplateResponse('index.html.jinja', template_data)

        def find_image_source_by_id(image_source_id: int) -> ImageSource:
            for image_source in self.slideshow.image_sources:
                if image_source.id == image_source_id:
                    return image_source
            return None

        @self.get('/image_sources/{image_source_id}/configuration.json')
        def serve_image_source_configuration(request: Request, image_source_id: int = None):
            image_source = find_image_source_by_id(image_source_id)
            if image_source is None:
                return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

            return image_source.get_configuration()


        @self.get('/image_sources/{image_source_id}/image.png', response_class=StreamingResponse)
        def serve_image_source_image(request: Request, image_source_id: int = None):
            image_source = find_image_source_by_id(image_source_id)
            if image_source is None:
                return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='image source not found')

            return image_response(image_source.get_image(self.screen.size))

        @self.route('/screen/image.png', methods=['GET'])
        def serve_screen_image(request: Request):
            return image_response(self.screen.image)

        @self.websocket_route("/ws", name="ws")
        class ClientSocketHandler(WebSocketEndpoint):
            encoding: str = "json"

            async def on_connect(self, websocket):
                logging.info("Connecting new user...")
                await websocket.accept()
                USERS.append(websocket)

            async def on_disconnect(self, websocket: WebSocket, close_code: int):
                logging.info("Disconnecting user...")
                USERS.remove(websocket)

            async def on_receive(self, websocket: WebSocket, msg: Any):
                logging.info("message received")
                logging.info(msg)
        
        @self.on_event('shutdown')
        async def shutdown():
            self.slideshow.stop()
            for user in USERS:
                if user.client_state == WebSocketState.CONNECTED:
                    await user.close()


    async def slideshow_update(self, slideshow: Slideshow) -> None:
        for websocket in USERS:
            await websocket.send_json({
                'type': 'slideshow',
                'image_source_index': slideshow.index,
                'image_source_id': slideshow.get_active_image_source().id
            })

    async def start(self, port: int) -> None:
        logging.info('Starting UI on port %d\n', port)
        config = uvicorn.Config(app=self, loop=asyncio.get_running_loop(), port=port, debug=True)
        server = uvicorn.Server(config)
        await server.serve()
