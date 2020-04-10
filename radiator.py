#!/usr/bin/env python
# pylint: disable=invalid-name,global-statement

from io import BytesIO
import os
from flask import Flask, render_template, send_file, send_from_directory
from image_sources.concourse.concourse import ConcourseContent
from image_sources.static_image.static_image import StaticImageContent

if os.environ.get('EINK_SCREEN_PRESENT'):
    from screen import Screen
else:
    from screen_fake import Screen

image = None
image_sources = [
    ConcourseContent(),
    StaticImageContent()
]
source_index = 0
screen = Screen()


def refresh():
    global image, source_index
    image = image_sources[source_index].get_image(screen.size())
    screen.set_image(image)


app = Flask(__name__)


@app.route('/', methods=['GET'])
def serve_controller_page():
    return render_template('index.html',
                           height=screen.size()[1],
                           width=screen.size()[0],
                           image_sources=image_sources
                           )


@app.route('/static/<path:filename>', methods=['GET'])
def serve_static_file(filename):
    return send_from_directory('static', filename, as_attachment=True)


@app.route('/radiator-image.png', methods=['GET'])
def serve_radiator_image():
    global image

    if image is not None:
        img_buffer = BytesIO()
        image.save(img_buffer, 'PNG')
        img_buffer.seek(0)
        return send_file(img_buffer, mimetype='image/png')
    return None, 404


if __name__ == '__main__':
    refresh()
    app.run(debug=os.environ.get('DEBUG', False))
