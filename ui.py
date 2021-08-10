# pylint: disable=global-statement
import asyncio
import logging
from typing import Any, List

from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocketState
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

import image_sources
from routers.image_source_router import ImageSourceRouter
from routers.screen_router import ScreenRouter
from routers.slideshow_router import SlideshowRouter
from screen import Screen, ScreenObserver
from slideshow import Slideshow, SlideshowObserver

USERS: List[WebSocket] = []

class ClientSocketHandler(WebSocketEndpoint):
    logger = logging.getLogger('websocket')
    encoding: str = "json"

    async def on_connect(self, websocket):
        self.logger.info('Connecting new user...')
        await websocket.accept()
        USERS.append(websocket)

    async def on_disconnect(self, websocket: WebSocket, close_code: int):
        self.logger.info('User disconnected (%d)', close_code)
        USERS.remove(websocket)

    async def on_receive(self, websocket: WebSocket, data: Any):
        self.logger.info('Message received: %s', data)


class UI(FastAPI, ScreenObserver, SlideshowObserver):
    logger = logging.getLogger('ui')
    templates = Jinja2Templates(directory='templates')

    def __init__(self, slideshow: Slideshow, screen: Screen):
        super().__init__(title="eInkRadiatorUI")

        self.mount("/static", StaticFiles(directory="static"), name="static")

        self.screen = screen
        self.screen.add_subscriber(self)
        self.slideshow = slideshow
        self.slideshow.add_subscriber(self)
        self.include_router(ImageSourceRouter(self.screen, self.slideshow))
        self.include_router(ScreenRouter(self.screen))
        self.include_router(SlideshowRouter(slideshow))
        self.router.add_websocket_route("/ws", ClientSocketHandler, name="ws")

        @self.get('/', response_class=HTMLResponse)
        def serve_ui(request: Request):
            template_data = {
                'request': request,
                'height': self.screen.size[1],
                'width': self.screen.size[0],
                'slideshow': self.slideshow
            }
            return self.templates.TemplateResponse('index.html.jinja', template_data)

        @self.on_event('shutdown')
        async def shutdown():
            self.slideshow.stop()
            for user in USERS:
                if user.client_state == WebSocketState.CONNECTED:
                    await user.close()

    async def send_message(self, message: Any) -> None:
        for websocket in USERS:
            await websocket.send_json(message)

    async def image_source_update(self, image_source: image_sources) -> None:
        await self.send_message({
            'type': 'image_source',
            'image_source_id': image_source.id
        })

    async def screen_update(self, screen: Screen) -> None:
        await self.send_message({
            'type': 'screen',
            'screen_busy': screen.busy
        })

    async def slideshow_update(self, slideshow: Slideshow) -> None:
        await self.send_message({
            'type': 'slideshow',
            'image_source_index': slideshow.index,
            'image_source_id': slideshow.get_active_image_source().id
        })

    async def start(self, port: int) -> None:
        self.logger.info('Starting UI on port %d', port)
        config = uvicorn.Config(
            app=self,
            loop=asyncio.get_running_loop(),
            host='0.0.0.0',
            port=port,
            debug=True
        )
        server = uvicorn.Server(config)
        await server.serve()
