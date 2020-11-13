from behave import *
from hamcrest import assert_that, is_, not_none
from selenium.webdriver.support.expected_conditions import title_is
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import requests
from features.environment import start_service
from time import sleep


@when('I view the page')
def step_impl(context):
    context.browser.implicitly_wait(5)  # seconds

    context.browser.get(context.url)

    wait = WebDriverWait(context.browser, 10)
    wait.until(title_is('eInk Radiator'))


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
    context.browser.find_element_by_id('add_source').click()


@when('I click delete')
def step_impl(context):
    context.browser.find_element_by_id('delete_source').click()


@when('I click save')
def step_impl(context):
    context.browser.find_element_by_id('saveConfig').click()


@when('I click the "set image" button')
def step_impl(context):
    context.browser.find_element_by_id('setImage').click()


@when('I select the red image source')
def step_impl(context):
    image_sources = Select(context.browser.find_element_by_id('image_sources'))
    image_sources.select_by_visible_text('Red')


@step('I change the name')
def step_impl(context):
    sleep(0.1)  # This is needed for the config to show up in the DOM
                # TODO: Change this to an eventually style test
    name_field = context.browser.find_element_by_name('name')
    name_field.clear()
    name_field.send_keys('my new name')


@then('new name shows up in the list')
def step_impl(context):
    source_selection = Select(context.browser.find_element_by_id('image_sources'))
    source_selection.select_by_visible_text('my new name')


@when('the service is restarted')
def step_impl(context):
    context.radiator_process.terminate()
    context.radiator_process.wait()
    context.radiator_process = start_service(context.port, context.url)


@then('the source has the new name')
def step_impl(context):
    source_selection = Select(context.browser.find_element_by_id('image_sources'))
    source_selection.select_by_visible_text('my new name')


@then('the preview image goes red')
def step_impl(context):
    sleep(0.1)
    preview_image = context.browser.find_element_by_id('preview-image')
    image = preview_image.value_of_css_property('background-image')
    assert_that(image, is_(context.fixtures['red_image']))


@then('the screen image goes red')
def step_impl(context):
    sleep(0.1)
    preview_image = context.browser.find_element_by_id('radiator-image')
    image = preview_image.value_of_css_property('background-image')
    assert_that(image, is_(context.fixtures['red_image']))
