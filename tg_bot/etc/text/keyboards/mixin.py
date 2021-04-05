import inspect
import random_data
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardsMixin:
    random_key_data = random_data.etc.password(length=20)

    def __init__(self, keys):
        self.keys = keys
        self.reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        self.close_on_click_reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        self.inline_keyboard = InlineKeyboardMarkup()

    def _get_this_keys(self, code_obj_name=None):
        if code_obj_name is None:
            code_obj_name = self._get_last_function_name(inspect.currentframe())

        response = self.keys[code_obj_name].copy()
        return response

    @staticmethod
    def _get_last_function_name(current_frame):
        caller_frame = current_frame.f_back
        code_obj = caller_frame.f_code
        code_obj_name = str(code_obj.co_name)
        return code_obj_name

    def _load_keys_in_reply_keyboard(self):
        this_keys = self._get_this_keys(code_obj_name=self._get_last_function_name(inspect.currentframe()))
        for keys_and_values in this_keys:
            only_keys = [value for _, value in keys_and_values.items()]
            self.reply_keyboard.row(*only_keys)

        return self.reply_keyboard

    def _load_keys_in_inline_keyboard(self, this_keys=None):
        if this_keys is None:
            last_function_name = self._get_last_function_name(inspect.currentframe())
            this_keys = self._get_this_keys(code_obj_name=last_function_name)

        for keys_and_values in this_keys:
            if isinstance(keys_and_values, list):
                keys = []
                for key, value in keys_and_values.items():
                    callback_data = "{}_{}".format(last_function_name, key)
                    keys.append(InlineKeyboardButton(value, callback_data=callback_data))

                self.inline_keyboard.add(*keys)

        return self.inline_keyboard


    @staticmethod
    def reformat_keys_dict(keys):
        _keys = {}

        for key, value in keys.items():
            _keys[key] = {}
            if isinstance(value, list):
                for values_dict in value:
                    for _key, _value in values_dict.items():
                        _keys[key][_key] = _value
            else:
                _keys[key] = value

        return _keys
