import os
import wrapcache
import importlib

from tg_bot.etc import utils
from . import default_settings


class Settings:
    def __init__(self):
        self.project_settings = importlib.import_module(os.environ.get("TG_BOT_SETTINGS_MODULE"))

        self.set_attributes(default_settings)
        self.set_attributes(self.project_settings)

    def set_attributes(self, module):
        for variable_name, variable in utils.get_variables_from_module(module):
            if isinstance(variable, dict) and self.project_settings == module:
                default_dict_variable = getattr(Settings, variable_name, {}).copy()
                default_dict_variable.update(variable)
                variable = default_dict_variable.copy()

            setattr(Settings, variable_name, variable)

            if "wrapcache_adapter" == variable_name:
                wrapcache.default_adapter = variable
