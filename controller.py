from flask import Flask, render_template, send_file
from io import BytesIO
from image_sources.image import ImageContent
from image_sources.concourse.concourse import ConcourseContent
from radiator import Radiator

app = Flask(__name__)

radiator = Radiator([
    ConcourseContent(),
    ImageContent()
])
radiator.refresh()

@app.route('/', methods=['GET'])
def serve_controller_page():
    return render_template('index.html')


@app.route('/radiator-image.png', methods=['GET'])
def serve_radiator_image():
    image = radiator.get_image()
    img_buffer = BytesIO()
    image.save(img_buffer, 'PNG')
    img_buffer.seek(0)
    return send_file(img_buffer, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
