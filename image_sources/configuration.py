from __future__ import annotations
from transpose import Transpose
from typing import Dict, List, Optional
from pydantic import BaseModel
from color import Color

#pylint: disable=too-few-public-methods
class ConfigurationField(BaseModel):
    type: Optional[str]
    value: str
    options: Optional[List[str]]

def new_color_configuration_field(value: Color) -> ConfigurationField:
    return ConfigurationField(type='color', value=value.name)

def new_hidden_configuration_field(value: str) -> ConfigurationField:
    return ConfigurationField(type='hidden', value=value)

def new_number_configuration_field(value: int) -> ConfigurationField:
    return ConfigurationField(type='number', value=str(value))

def new_select_configuration_field(value: str, options: List[str]) -> ConfigurationField:
    return ConfigurationField(type='select', value=value, options=options)

def new_text_configuration_field(value: str) -> ConfigurationField:
    return ConfigurationField(type='text', value=value)

def new_textarea_configuration_field(value: str) -> ConfigurationField:
    return ConfigurationField(type='textarea', value=value)

def new_transform_configuration_field(value: Transpose) -> ConfigurationField:
    return ConfigurationField(type='transform', value=value.name)

#pylint: disable=too-few-public-methods
class Configuration(BaseModel):
    type: Optional[str]
    data: Dict[str, ConfigurationField] = {}

    def update(self, new_configuration: Configuration) -> bool:
        changed = False
        for key, config_field in self.data.items():
            if key in new_configuration.data and config_field.value != new_configuration.data[key].value:
                config_field.value = new_configuration.data[key].value
                changed = True

        return changed

    def get(self, key: str) -> str:
        if self.data[key] is not None:
            return self.data[key].value
        return ''
