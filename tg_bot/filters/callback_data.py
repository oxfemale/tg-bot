"""
Делаю как https://github.com/aiogram/aiogram/blob/dev-2.x/aiogram/utils/callback_data.py
"""

import typing
from aiogram import types
from aiogram.dispatcher.filters import Filter

from tg_bot.etc.database import callback_data_filter


class CallbackData:
    """
    Callback data factory
    """

    def __init__(self, *parts, **kwargs):
        self._part_names = parts
        self._default_part_names = kwargs

    def new(self, **kwargs):
        """
        Generate callback data
        :param kwargs:
        :return:
        """
        default_part_names = self._default_part_names.copy()
        default_part_names.update(kwargs)
        data = kwargs.copy()

        for part in self._part_names:
            if part in kwargs:
                del kwargs[part]
            else:
                raise ValueError("Value for {} was not passed!".format(part))

        if kwargs:
            raise TypeError("Too many arguments were passed!")

        return callback_data_filter.write_data(data)

    @staticmethod
    def parse(code):
        return callback_data_filter.get_data(code)

    def filter(self, **config):
        """
        Generate filter
        :param config:
        :return:
        """
        for key in config.keys():
            if key not in self._part_names:
                raise ValueError(f"Invalid field name {key!r}")
        return CallbackDataFilter(self, config)


class CallbackDataFilter(Filter):
    def __init__(self, factory: CallbackData, config: typing.Dict[str, str]):
        self.config = config
        self.factory = factory

    @classmethod
    def validate(cls, full_config: typing.Dict[str, typing.Any]):
        raise ValueError("That filter can't be used in filters factory!")

    async def check(self, callback: types.CallbackQuery):
        data = self.factory.parse(callback.data)

        part_names = list(self.factory._part_names) + list(self.factory._default_part_names.keys())

        if data is not None and list(data.keys()) == part_names:
            if data:
                response = lambda: None

                for key, value in data.items():
                    setattr(response, key, value)
                for key, value in self.config.items():
                    if isinstance(value, (list, tuple, set, frozenset)):
                        if data.get(key) not in value:
                            return False
                    else:
                        if data.get(key) != value:
                            return False

                response = {"callback_data": response}
            else:
                response = False

        else:
            response = False

        return response