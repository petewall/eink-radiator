#!/usr/bin/env python
# pylint: disable=invalid-name,global-statement,line-too-long

from io import BytesIO
import pickle
import os
from flask import Flask, jsonify, make_response, render_template, request, send_file, send_from_directory

from image_sources.blank import White, Black, Red
from image_sources.image import ImageContent
from image_sources.concourse.concourse import ConcourseContent
from image_sources.text import TextContent

if os.environ.get('EINK_SCREEN_PRESENT'):
    from inky_screen import InkyScreen
    screen = InkyScreen()
else:
    from screen import Screen
    screen = Screen()

source_types = [
    ConcourseContent,
    ImageContent,
    TextContent
]
state = {
    'current_image': None,
    'image_sources': [
        White(),
        Black(),
        Red()
    ],
    'source_index': 0
}


def get_image_source():
    if state['source_index'] is None:
        return None
    return state['image_sources'][state['source_index']]


def save():
    picklefile = open("radiator.pickle", 'wb')
    pickle.dump(state, picklefile)
    picklefile.close()


def load():
    global state
    if os.path.isfile("radiator.pickle"):
        picklefile = open("radiator.pickle", 'rb')
        state = pickle.load(picklefile)
        picklefile.close()


def refresh():
    global state
    image_source = get_image_source()
    if image_source is not None:
        new_image = image_source.get_image(screen.size())
        if new_image is not None:
            state['current_image'] = new_image


app = Flask(__name__)


@app.route('/', methods=['GET'])
def serve_controller_page():
    return render_template('index.html',
                           height=screen.size()[1],
                           width=screen.size()[0],
                           image_sources=state['image_sources'],
                           source_index=state['source_index'],
                           source_types=source_types
                           )


@app.route('/static/<path:filename>', methods=['GET'])
def serve_static_file(filename):
    return send_from_directory('static', filename, as_attachment=True)


def image_response(image):
    if image is None:
        return make_response('', 204)

    img_buffer = BytesIO()
    image.save(img_buffer, 'PNG')
    img_buffer.seek(0)
    response = make_response(send_file(img_buffer, mimetype='image/png'))
    response.headers['Cache-Control'] = 'no-cache'
    return response


@app.route('/preview-image.png', methods=['GET'])
def serve_image():
    return image_response(state['current_image'])


@app.route('/radiator-image.png', methods=['GET'])
def serve_screen_image():
    return image_response(screen.get_image())


@app.route('/source', methods=['GET'])
def get_source_config():
    return jsonify(get_image_source().get_configuration())


@app.route('/source', methods=['POST'])
def add_image_source():
    body = request.json
    new_source_index = body.get('index')
    config = body.get('config', {})
    state['image_sources'].append(source_types[new_source_index](config))
    save()
    return make_response('', 200)


@app.route('/source', methods=['DELETE'])
def delete_image_source():
    state['image_sources'].pop(state['source_index'])
    if state['source_index'] == len(state['image_sources']):
        state['source_index'] -= 1
    refresh()
    save()
    return make_response('', 200)


@app.route('/source', methods=['PATCH'])
def set_source_config():
    config = request.json
    get_image_source().set_configuration(config)
    refresh()
    save()
    return make_response('', 200)


@app.route('/select_source/<index>', methods=['POST'])
def choose_source(index=None):
    if index is None:
        return 'missing source index', 400

    index = int(index)
    if index < 0 or index > len(state['image_sources']):
        return 'source index out of range', 400

    state['source_index'] = index
    refresh()
    return make_response('', 200)


@app.route('/set_image', methods=['POST'])
def display_image():
    screen.set_image(state['current_image'])
    return '', 200


if __name__ == '__main__':
    load()
    refresh()
    port = os.environ.get('PORT', 5000)
    print(f'Starting server on port {port}...')
    app.run(debug=os.environ.get('DEBUG', False), host='0.0.0.0', port=port)
