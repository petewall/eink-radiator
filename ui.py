from io import BytesIO
import logging
import os
from screen import Screen
from slideshow import Slideshow, SlideshowObserver
from flask import Flask, make_response, render_template, send_file

app = Flask(__name__)
ui_instance = None

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
    global ui_instance
    ui_instance = self
    logging.info('Starting UI on port %d\n', port)
    app.run(debug=os.environ.get('DEBUG', False), host='0.0.0.0', port=port)



@app.route('/', methods=['GET'])
def serve_ui():
  return render_template(
    'index.html.jinja',
    height=ui_instance.screen.size[1],
    width=ui_instance.screen.size[0],
    slideshow=ui_instance.slideshow
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

@app.route('/image_sources/<int:image_source_id>/image.png', methods=['GET'])
def serve_image_source_image(image_source_id: int = None):
  for image_source in ui_instance.slideshow.image_sources:
    if image_source.id == image_source_id:
      image = image_source.get_image(ui_instance.screen.size)
      return image_response(image)

  return make_response('image source not found', 404)

@app.route('/screen/image.png', methods=['GET'])
def serve_screen_image():
  return image_response(ui_instance.screen.image)