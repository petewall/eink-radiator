#!/usr/bin/env python
# pylint: disable=invalid-name,global-statement

from io import BytesIO
import os
from flask import Flask, jsonify, make_response, render_template, request, send_file, send_from_directory

from image_sources.Image import ImageContent
from image_sources.concourse.concourse import ConcourseContent
from image_sources.static_image.static_image import StaticImageContent

if os.environ.get('EINK_SCREEN_PRESENT'):
    from screen import Screen
else:
    from screen_null import Screen

image = None
image_sources = [
    ImageContent(
        {
            'name': 'Raspberry Pi',
            'url': 'https://mastersofmedia.hum.uva.nl/wp-content/uploads/2014/09/Raspberry-Pi-Logo1-620x350.png'
        }),
    # ConcourseContent(),
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
                           image_sources=image_sources,
                           source_index=source_index
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
        response = make_response(send_file(img_buffer, mimetype='image/png'))
        response.headers['Cache-Control'] = 'no-cache'
        return response
    return None, 404


@app.route('/source', methods=['GET'])
def get_source_config():
    global image_sources, source_index
    return jsonify(image_sources[source_index].get_configuration())


@app.route('/source', methods=['PATCH'])
def set_source_config():
    config = request.json
    image_sources[source_index].set_configuration(config)
    refresh()
    return '', 200


@app.route('/select_source/<index>', methods=['POST'])
def choose_source(index=None):
    if index is None:
        return 'missing source index', 400

    index = int(index)
    if index < 0 or index > len(image_sources):
        return 'source index out of range', 400

    global source_index
    source_index = index
    refresh()
    return '', 200


if __name__ == '__main__':
    refresh()
    app.run(debug=os.environ.get('DEBUG', False))
