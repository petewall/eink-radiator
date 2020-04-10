#!/usr/bin/env python
# pylint: disable=invalid-name

from io import BytesIO
import os
from flask import Flask, render_template, send_file
from image_sources.image import ImageContent
from image_sources.concourse.concourse import ConcourseContent
if os.environ.get('EINK_SCREEN_PRESENT'):
    from screen import Screen
else:
    from screen_fake import Screen

image_sources = [
    ConcourseContent(),
    ImageContent()
]
source_index = 0
screen = Screen()
image = image_sources[source_index].get_image(screen.size())
screen.set_image(image)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def serve_controller_page():
    return render_template('index.html')


@app.route('/radiator-image.png', methods=['GET'])
def serve_radiator_image():
    img_buffer = BytesIO()
    image.save(img_buffer, 'PNG')
    img_buffer.seek(0)
    return send_file(img_buffer, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
