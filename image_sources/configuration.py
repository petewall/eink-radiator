from __future__ import annotations
from typing import Dict, List, Optional
from pydantic import BaseModel
from color import Color

#pylint: disable=too-few-public-methods
class ConfigurationField(BaseModel):
    type: Optional[str]
    value: str
    options: Optional[List[str]]

def new_color_configuration_field(value: Color) -> ConfigurationField:
    return ConfigurationField(type='select', value=value.name, options=Color.all_colors())

def new_text_configuration_field(value: str) -> ConfigurationField:
    return ConfigurationField(type='text', value=value)

def new_textarea_configuration_field(value: str) -> ConfigurationField:
    return ConfigurationField(type='textarea', value=value)

#pylint: disable=too-few-public-methods
class Configuration(BaseModel):
    id: Optional[int]
    name: Optional[str]
    data: Optional[Dict[str, ConfigurationField]] = {}

    def update(self, new_configuration: Configuration) -> bool:
        changed = False
        if self.name != new_configuration.name:
            self.name = new_configuration.name
            changed = True

        for key in self.data:
            if self.data[key].value != new_configuration.data[key].value:
                self.data[key].value = new_configuration.data[key].value
                changed = True

        return changed
