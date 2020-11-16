import os
import base64
from behave import fixture, use_fixture
from behave.model_core import Status
import subprocess
from time import sleep

from selenium import webdriver
import requests
from get_port import find_free_port
from hamcrest import assert_that, instance_of, is_


def start_service(port, url):
    env = os.environ.copy()
    env['PORT'] = str(port)

    radiator_process = subprocess.Popen(
        ['python', 'radiator.py'],
        env=env
    )

    response = get(url)
    while response.status_code != 200:
        sleep(0.5)
        response = get(url)

    return radiator_process


def get(url):
    try:
        return requests.get(url)
    except Exception:
        # sleep for a bit in case that helps
        sleep(0.25)
        # try again
        return get(url)


@fixture
def service_hook(context, port=5000):
    if os.path.isfile('radiator.pickle'):
        os.remove('radiator.pickle')
    context.port = port
    context.url = f'http://localhost:{port}'
    context.radiator_process = start_service(port, context.url)

    yield context.radiator_process

    context.radiator_process.terminate()
    context.radiator_process.wait()


@fixture
def start_browser(context):
    options = webdriver.ChromeOptions()
    if os.getenv('CI') is not None:
        options.add_argument('headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

    context.browser = webdriver.Chrome(chrome_options=options)

    yield context.browser

    context.browser.quit()


@fixture
def load_test_fixtures(context):
    static_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'static')
    red_image_file = open(os.path.join(static_dir, 'red.png'), 'rb')
    red_image_encoded = str(base64.b64encode(red_image_file.read()), 'utf-8')
    red_image_file.close()

    white_image_file = open(os.path.join(static_dir, 'white.png'), 'rb')
    white_image_encoded = str(base64.b64encode(white_image_file.read()), 'utf-8')
    white_image_file.close()

    test_fixtures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'test_fixtures')
    text_image_file = open(os.path.join(test_fixtures_dir, 'text_1.png'), 'rb')
    text_image_encoded = str(base64.b64encode(text_image_file.read()), 'utf-8')
    text_image_file.close()

    context.fixtures = {
        'red_image': 'url("data:image/png;base64,{}")'.format(red_image_encoded),
        'text_image': 'url("data:image/png;base64,{}")'.format(text_image_encoded),
        'white_image': 'url("data:image/png;base64,{}")'.format(white_image_encoded)
    }


def before_all(context):
    use_fixture(start_browser, context)
    use_fixture(load_test_fixtures, context)


def before_feature(context, _):
    port, error = find_free_port()
    assert_that(port, is_(instance_of(int)))
    assert_that(error, is_({}))
    use_fixture(service_hook, context, port=port)


def after_feature(context, feature):
    if feature.status == Status.failed:
        context.browser.get_screenshot_as_file("screenshot.png")
