from behave import given, then, when # pylint: disable=no-name-in-module
from hamcrest import assert_that, calling, is_, raises
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import requests
from time import sleep
from radiator import source_types # pylint: disable=import-error
from image_sources.text import TextContent # pylint: disable=import-error


@given('a text source exists')
def a_text_source_exists(context):
    requests.post(context.url + '/source', json={
        'index': source_types.index(TextContent),
        'config': {
            'name': 'test text content',
            'text': 'initial text content'
        }
    })


@when('I select TextContent from the new source dropdown')
def i_select_textcontent_from_the_new_source_dropdown(context):
    new_source_dropdown = Select(context.browser.find_element_by_id('new_source_list'))
    new_source_dropdown.select_by_value('TextContent')


@when('I select the text source')
def i_select_the_text_source(context):
    source_selection = Select(context.browser.find_element_by_id('image_sources'))
    source_selection.select_by_visible_text('test text content')


@when('I change the text')
def i_change_the_text(context):
    sleep(0.1)  # This is needed for the config to show up in the DOM
                # TODO: Change this to an eventually style test
    name_field = context.browser.find_element_by_name('text')
    name_field.clear()
    name_field.send_keys('It is now safe to turn off your computer')


@then('a new text source is added')
def a_new_text_source_is_added(context):
    source_selection = Select(context.browser.find_element_by_id('image_sources'))
    source_selection.select_by_visible_text('New TextContent')


@then('the text source is removed')
def the_text_source_is_removed(context):
    source_selection = Select(context.browser.find_element_by_id('image_sources'))
    assert_that(
        calling(source_selection.select_by_visible_text)
        .with_args('test text content'),
        raises(NoSuchElementException))


@then('the preview image shows the text image')
def the_preview_image_shows_the_text_image(context):
    sleep(0.1)  # This is needed for the config to show up in the DOM
                # TODO: Change this to an eventually style test
    preview_image = context.browser.find_element_by_id('preview-image')
    image = preview_image.value_of_css_property('background-image')
    assert_that(image, is_(context.fixtures['text_image']))


@then('the screen image shows the same image')
def the_screen_image_shows_the_same_image(context):
    sleep(0.1)  # This is needed for the config to show up in the DOM
                # TODO: Change this to an eventually style test
    preview_image = context.browser.find_element_by_id('radiator-image')
    image = preview_image.value_of_css_property('background-image')
    assert_that(image, is_(context.fixtures['text_image']))
