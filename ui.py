# pylint: disable=global-statement
from io import BytesIO
import logging
import os
from flask import Flask, jsonify, make_response, render_template, send_file
from screen import Screen
from slideshow import Slideshow, SlideshowObserver

app = Flask(__name__)
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
        app.run(debug=os.environ.get('DEBUG', False), host='0.0.0.0', port=port)



@app.route('/', methods=['GET'])
def serve_ui():
    return render_template(
        'index.html.jinja',
        height=UI_INSTANCE.screen.size[1],
        width=UI_INSTANCE.screen.size[0],
        slideshow=UI_INSTANCE.slideshow
    )

def image_response(image):
    if image is None:
        return make_response('', 204)

    img_buffer = BytesIO()
    image.save(img_buffer, 'PNG')
    img_buffer.seek(0)
    response = make_response(send_file(img_buffer, mimetype='image/png'))
    response.headers['Cache-Control'] = 'no-cache'
    return response

@app.route('/image_sources/<int:image_source_id>/configuration.json', methods=['GET'])
def serve_image_source_configuration(image_source_id: int = None):
    for image_source in UI_INSTANCE.slideshow.image_sources:
        if image_source.id == image_source_id:
            return jsonify(image_source.get_configuration())

    return make_response('image source not found', 404)

@app.route('/image_sources/<int:image_source_id>/image.png', methods=['GET'])
def serve_image_source_image(image_source_id: int = None):
    for image_source in UI_INSTANCE.slideshow.image_sources:
        if image_source.id == image_source_id:
            image = image_source.get_image(UI_INSTANCE.screen.size)
            return image_response(image)

    return make_response('image source not found', 404)

@app.route('/screen/image.png', methods=['GET'])
def serve_screen_image():
    return image_response(UI_INSTANCE.screen.image)
