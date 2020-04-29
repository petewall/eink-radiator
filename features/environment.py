import os
from behave import *
import subprocess
from time import sleep
from selenium import webdriver
import requests
from get_port import find_free_port
from hamcrest import *


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
    if os.path.isfile("radiator.pickle"):
        os.remove('radiator.pickle')
    context.port = port
    context.url = f'http://localhost:{port}'
    context.radiator_process = start_service(port, context.url)

    yield context.radiator_process

    context.radiator_process.terminate()
    context.radiator_process.wait()


@fixture
def start_browser(context):
    context.browser = webdriver.Chrome()

    yield context.browser

    context.browser.quit()


def before_all(context):
    use_fixture(start_browser, context)


def before_feature(context, _):
    port, error = find_free_port()
    assert_that(port, is_(instance_of(int)))
    assert_that(error, is_({}))
    use_fixture(service_hook, context, port=port)
