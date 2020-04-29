import os
import subprocess
from behave import *
from hamcrest import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.expected_conditions import title_is
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import requests
from features.environment import start_service


@when('I view the page')
def step_impl(context):
    context.browser.implicitly_wait(5)  # seconds

    context.browser.get(context.url)

    wait = WebDriverWait(context.browser, 10)
    wait.until(title_is('eInk Radiator'))


@when('I select TextContent from the new source dropdown')
def step_impl(context):
    new_source_dropdown = Select(context.browser.find_element_by_id('new_source_list'))
    new_source_dropdown.select_by_value('TextContent')


@then('the add button is enabled')
def step_impl(context):
    add_button = context.browser.find_element_by_id('add_source')
    assert_that(add_button.is_enabled(), is_(True))


@then('the add button is disabled')
def step_impl(context):
    add_button = context.browser.find_element_by_id('add_source')
    assert_that(add_button.is_enabled(), is_(False))


@then('I can see the current image')
def step_impl(context):
    assert_that(context.browser.find_element_by_id('radiator-image'), is_(not_none()))


@then('I can see the preview image')
def step_impl(context):
    assert(context.browser.find_element_by_id('preview-image'))


@then('I can see the list of image sources')
def step_impl(context):
    assert(context.browser.find_element_by_id('image_sources'))


@step('I click add')
def step_impl(context):
    add_button = context.browser.find_element_by_id('add_source')
    add_button.click()


@then('a new text source is added')
def step_impl(context):
    source_selection = Select(context.browser.find_element_by_id('image_sources'))
    source_selection.select_by_visible_text('New TextContent')


@step('I select the text source')
def step_impl(context):
    source_selection = Select(context.browser.find_element_by_id('image_sources'))
    source_selection.select_by_visible_text('test text content')


@step('I click delete')
def step_impl(context):
    add_button = context.browser.find_element_by_id('delete_source')
    add_button.click()


@then('the text source is removed')
def step_impl(context):
    source_selection = Select(context.browser.find_element_by_id('image_sources'))
    assert_that(
        calling(source_selection.select_by_visible_text)
        .with_args('test text content'),
        raises(NoSuchElementException))


@given('a text source exists')
def step_impl(context):
    requests.post(context.url + '/source', json={
        'index': 2,
        'config': {
            'name': 'test text content'
        }
    })


@step('I change the name')
def step_impl(context):
    name_field = context.browser.find_element_by_name('name')
    name_field.clear()
    name_field.send_keys('my new name')
    context.browser.find_element_by_id('saveConfig').click()


@then('new name shows up in the list')
def step_impl(context):
    source_selection = Select(context.browser.find_element_by_id('image_sources'))
    source_selection.select_by_visible_text('my new name')


@when('the service is restarted')
def step_impl(context):
    context.radiator_process.terminate()
    context.radiator_process.wait()
    context.radiator_process = start_service(context.port, context.url)


@then('the text source has the new name')
def step_impl(context):
    source_selection = Select(context.browser.find_element_by_id('image_sources'))
    source_selection.select_by_visible_text('my new name')
