from behave import *
from hamcrest import assert_that, calling, is_, raises
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import requests
from time import sleep
from radiator import source_types
from image_sources.slideshow import SlideshowContent


@given('a slideshow source exists')
def step_impl(context):
    requests.post(context.url + '/source', json={
        'index': source_types.index(SlideshowContent),
        'config': {
            'name': 'test slideshow content'
        }
    })


@when('I set two image URLs')
def step_impl(context):
    sleep(0.1)  # This is needed for the config to show up in the DOM
                # TODO: Change this to an eventually style test
    image_urls_field = context.browser.find_element_by_name('images')
    image_urls_field.clear()
    image_urls_field.send_keys(f'{context.url}/white.png\n{context.url}/red.png')


@when('I change the interval to 1 second')
def step_impl(context):
    interval_field = context.browser.find_element_by_name('interval')
    interval_field.clear()
    interval_field.send_keys('1')


@when('I select the slideshow source')
def step_impl(context):
    source_selection = Select(context.browser.find_element_by_id('image_sources'))
    source_selection.select_by_visible_text('test slideshow content')


@when('I wait for 1.5 seconds')
def step_impl(context):
    sleep(1.5)


@then('the screen shows the first image')
def step_impl(context):
    sleep(0.1)
    preview_image = context.browser.find_element_by_id('preview-image')
    image = preview_image.value_of_css_property('background-image')
    assert_that(image, is_(context.fixtures['red_image']))


@then('the screen image shows the second image')
def step_impl(context):
    sleep(0.1)
    preview_image = context.browser.find_element_by_id('preview-image')
    image = preview_image.value_of_css_property('background-image')
    assert_that(image, is_(context.fixtures['white_image']))

