from routers.helpers import image_response
from fastapi import APIRouter, Request
from screen import Screen

class ScreenRouter(APIRouter):
    def __init__(self, screen: Screen):
        super().__init__()
        self.screen = screen

        @self.route('/screen/image.png', methods=['GET'])
        def serve_screen_image(request: Request):
            return image_response(self.screen.image)

