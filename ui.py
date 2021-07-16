# pylint: disable=global-statement
import asyncio
from routers.screen_router import ScreenRouter
from routers.image_source_router import ImageSourceRouter
from typing import Any, List

from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocketState
import logging
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from screen import Screen, ScreenObserver
from slideshow import Slideshow, SlideshowObserver

USERS: List[WebSocket] = []

class UI(FastAPI, ScreenObserver, SlideshowObserver):
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

    async def screen_update(self, screen: Screen) -> None:
        for websocket in USERS:
            await websocket.send_json({
                'type': 'screen',
                'screen_busy': screen.busy
            })

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
