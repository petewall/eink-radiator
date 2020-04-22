#!/usr/bin/env python
# pylint: disable=invalid-name,global-statement,line-too-long

from io import BytesIO
import os
from flask import Flask, jsonify, make_response, render_template, request, send_file, send_from_directory

from image_sources.image import ImageContent
from image_sources.concourse.concourse import ConcourseContent
from image_sources.static_image import StaticImageContent
from image_sources.text import TextContent

if os.environ.get('EINK_SCREEN_PRESENT'):
    from screen import Screen
else:
    from screen_null import Screen

current_image = None
image_sources = [
    ImageContent({
        'name': 'Raspberry Pi',
        'url': 'https://mastersofmedia.hum.uva.nl/wp-content/uploads/2014/09/Raspberry-Pi-Logo1-620x350.png'
    }),
    ConcourseContent({
        'name': 'Concourse',
        'url': 'https://ci.wallserver.local'
    }),
    StaticImageContent({
        'name': 'Inky',
        'image_path': 'test_fixtures/InkywHAT-400x300.png'
    }),
    TextContent({
        'name': 'Message',
        'text': 'Lorem Ipsum'
    }),
]
source_index = 0
screen = Screen()


def refresh():
    global current_image, source_index
    current_image = image_sources[source_index].get_image(screen.size())


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


def image_response(image):
    if image is None:
        return make_response('', 404)

    img_buffer = BytesIO()
    image.save(img_buffer, 'PNG')
    img_buffer.seek(0)
    response = make_response(send_file(img_buffer, mimetype='image/png'))
    response.headers['Cache-Control'] = 'no-cache'
    return response


@app.route('/preview-image.png', methods=['GET'])
def serve_image():
    global current_image
    return image_response(current_image)


@app.route('/radiator-image.png', methods=['GET'])
def serve_screen_image():
    global screen
    return image_response(screen.get_image())


@app.route('/source', methods=['GET'])
def get_source_config():
    global image_sources, source_index
    return jsonify(image_sources[source_index].get_configuration())


@app.route('/source', methods=['PATCH'])
def set_source_config():
    config = request.json
    image_sources[source_index].set_configuration(config)
    refresh()
    return make_response('', 200)


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
    return make_response('', 200)


@app.route('/set_image', methods=['POST'])
def display_image():
    global current_image, screen
    screen.set_image(current_image)
    return '', 200


if __name__ == '__main__':
    refresh()
    app.run(debug=os.environ.get('DEBUG', False), host='0.0.0.0', port=os.environ.get('PORT', 5000))
