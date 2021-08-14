#pylint: disable=no-self-use
import json
import unittest
from hamcrest import assert_that, equal_to, is_
from color import Color
from image_sources.configuration import Configuration, new_color_configuration_field, new_text_configuration_field, new_textarea_configuration_field


class TestConfigurationField(unittest.TestCase):
    def test_new_color_configuration_field(self):
        field = new_color_configuration_field(Color.RED)
        assert_that(field.type, is_(equal_to('select')))
        assert_that(field.value, is_(equal_to('RED')))
        assert_that(field.options, is_(equal_to(Color.all_colors())))

    def test_new_text_configuration_field(self):
        field = new_text_configuration_field('pete')
        assert_that(field.type, is_(equal_to('text')))
        assert_that(field.value, is_(equal_to('pete')))

    def test_new_textarea_configuration_field(self):
        field = new_textarea_configuration_field('pete\nwall')
        assert_that(field.type, is_(equal_to('textarea')))
        assert_that(field.value, is_(equal_to('pete\nwall')))

class TestConfiguration(unittest.TestCase):
    def test_update(self):
        config = Configuration(data={
            'name': new_text_configuration_field('pete')
        })
        new_config = Configuration(data={
            'name': new_text_configuration_field('peter wall')
        })

        changed = config.update(config)
        assert_that(changed, is_(equal_to(False)))

        changed = config.update(new_config)
        assert_that(changed, is_(equal_to(True)))
        assert_that(config.data['name'].value, is_(equal_to('peter wall')))

    def test_serialization(self):
        config = Configuration(data={
            'name': new_text_configuration_field('pete')
        })

        serialized = config.json(exclude_none=True)
        assert_that(serialized, is_(equal_to('{"data": {"name": {"type": "text", "value": "pete"}}}')))

    def test_deserialization(self):
        serialized = json.dumps({
            'data': {
                'name': {
                    'type': 'text',
                    'value': 'pete'
                }
            }
        })

        config = Configuration.parse_raw(serialized)
        assert_that(config.data['name'].value, is_(equal_to('pete')))
