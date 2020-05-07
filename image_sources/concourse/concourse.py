import os
from PIL import Image, ImageDraw, ImageFont
import requests
from image_sources.image_source import ImageSource
from color import Color

FONT_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..', 'RobotoSlab-Regular.ttf'
)


class ConcourseContent(ImageSource):
    url = None
    username = None
    password = None
    auth_token = None
    title_font = ImageFont.truetype(font=FONT_PATH, size=30)
    content_font = ImageFont.truetype(font=FONT_PATH, size=15)

    def get_configuration(self):
        return {
            'name': self.name,
            'url': self.url,
            'username': self.username,
            'password': self.password
        }

    def set_configuration(self, params):
        super().set_configuration(params)
        if params.get('url') is not None:
            self.url = params.get('url')
        if params.get('username') is not None:
            self.username = params.get('username')
        if params.get('password') is not None:
            self.password = params.get('password')

    def auth(self):
        session = requests.Session()
        session.auth = ('fly', 'Zmx5')
        data = {
            'grant_type': 'password',
            'password': self.password,
            'username': self.username,
            'scope': 'openid profile email federated:id groups'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        auth_response = session.post(self.url + '/sky/token', headers=headers, data=data).json()
        self.auth_token = auth_response['access_token']

    def get_pipeline_status(self):
        if self.auth_token is None:
            self.auth()
        headers = {'Authorization': 'Bearer ' + self.auth_token}
        jobs = requests.get(self.url + '/api/v1/jobs', headers=headers).json()

        pipelines = {}
        for job in jobs:
            name = job.get('pipeline_name')
            if pipelines.get(name) is None:
                pipelines[name] = True
            if job.get('finished_build', {}).get('status', False) != 'succeeded':
                pipelines[name] = False
        return pipelines

    def get_image(self, size):
        if self.url is None or self.url == '':
            raise ValueError('Concourse URL is required')
        if self.username is None or self.username == '':
            raise ValueError('Concourse username is required')
        if self.password is None or self.password == '':
            raise ValueError('Concourse password is required')

        image = Image.new('P', size, Color.black.value)
        image.putpalette(Color.palette())

        logo = Image.open("image_sources/concourse/logo.png")
        image.paste(logo, box=(5, 5, 40, 40), mask=logo)

        image_canvas = ImageDraw.Draw(image)
        image_canvas.text((45, 3), 'Concourse', fill=Color.white.value, font=self.title_font)
        image_canvas.line([(5, 47), (395, 47)], fill=Color.red.value, width=2)

        pipelines = self.get_pipeline_status()
        pipeline_names = list(pipelines.keys())
        pipeline_names.sort()
        y_pos = 50
        for pipeline in pipeline_names:
            success = pipelines[pipeline]
            color = Color.white if success else Color.red
            image_canvas.text((5, y_pos), pipeline, fill=color.value, font=self.content_font)
            y_pos += 17

        return image
