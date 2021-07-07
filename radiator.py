#!/usr/bin/env python
# pylint: disable=invalid-name,global-statement,line-too-long

import logging
from io import BytesIO
import pickle
import os
from flask import Flask, jsonify, make_response, render_template, request, send_file, send_from_directory

from image_sources.blank import White, Black, Red
# from image_sources.concourse.concourse import ConcourseContent
from image_sources.image import ImageContent
from image_sources.text import TextContent
from image_sources.weather.weather import WeatherContent
from screen import Screen

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

if os.environ.get('EINK_SCREEN_PRESENT'):
    from inky_screen import InkyScreen
    screen = InkyScreen()
    preview_screen = Screen(screen.size)
else:
    screen = Screen((400, 300))
    preview_screen = Screen((400, 300))

source_types = [
    ImageContent,
    TextContent,
    WeatherContent
]
state = {
    'image_sources': [
        WeatherContent({ 'name': 'Weather' }),
        White(),
        Black(),
        Red()
    ],
    'preview_image_source': 0,
    'screen_image_source': 0
}


def get_preview_image_source():
    if state.get('preview_image_source') is None:
        return None
    return state['image_sources'][state['preview_image_source']]


def get_screen_image_source():
    if state.get('screen_image_source') is None:
        return None
    return state['image_sources'][state['screen_image_source']]


data_file_path = os.environ.get('DATA_FILE_PATH') or os.path.join(os.getcwd(), 'radiator.pickle')


def save():
    with open(data_file_path, 'wb') as picklefile:
        pickle.dump(state, picklefile)
        picklefile.close()


def load():
    global state
    if os.path.isfile(data_file_path):
        with open(data_file_path, 'rb') as picklefile:
            state = pickle.load(picklefile)
            picklefile.close()

        screen.set_image_source(get_screen_image_source())
        preview_screen.set_image_source(get_preview_image_source())


app = Flask(__name__)


@app.route('/', methods=['GET'])
def serve_controller_page():
    return render_template(
        'index.html',
        height=screen.size[1],
        width=screen.size[0],
        image_sources=state['image_sources'],
        preview_image_source=state['preview_image_source'],
        screen_image_source=state['screen_image_source'],
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
def serve_preview_image():
    return image_response(preview_screen.image)


@app.route('/radiator-image.png', methods=['GET'])
def serve_screen_image():
    return image_response(screen.image)


@app.route('/source', methods=['GET'])
def get_source_config():
    return jsonify(get_preview_image_source().get_configuration())


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
    index = state['preview_image_source']
    state['image_sources'].pop(index)

    if state['screen_image_source'] is not None:
        if state['screen_image_source'] == index:
            state['screen_image_source'] = None
            screen.set_image_source(None)
        if state['screen_image_source'] > index:
            state['screen_image_source'] -= 1
    save()
    return make_response('', 200)


@app.route('/source', methods=['PATCH'])
def set_source_config():
    config = request.json
    get_preview_image_source().set_configuration(config)
    preview_screen.refresh()
    save()
    return make_response('', 200)


@app.route('/select_source/<index>', methods=['POST'])
def select_source(index=None):
    if index is None:
        return 'missing source index', 400

    index = int(index)
    if index < 0 or index > len(state['image_sources']):
        return 'source index out of range', 400

    state['preview_image_source'] = index
    preview_screen.set_image_source(get_preview_image_source())
    save()
    return make_response('', 200)


@app.route('/set_image', methods=['POST'])
def set_image_source():
    global state
    index = state['preview_image_source']
    state['screen_image_source'] = index
    screen.set_image_source(get_screen_image_source())
    save()
    return '', 200


if __name__ == '__main__':
    load()
    port = os.environ.get('PORT', 5000)
    print(f'Starting server on port {port}...')
    app.run(debug=os.environ.get('DEBUG', False), host='0.0.0.0', port=port)
