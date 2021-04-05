"""
Делал смотря на:
https://github.com/aiogram/aiogram/blob/dev-2.x/aiogram/contrib/fsm_storage/rethinkdb.py
"""

import typing
import inspect
from abc import ABC
from aiogram.dispatcher.storage import BaseStorage

from ..etc.database import state as state_actions


class PeeweeORMStorage(BaseStorage, ABC):
    def __init__(self, bot_id=1):
        """
        Добавить параметр, для возможности установки имени таблицы
        def __init__(self, table: str = "temp"):
        """
        self.bot_id = bot_id

    async def get_state(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                        default: typing.Optional[str] = None) -> typing.Optional[str]:
        return self._execute(chat, user)

    async def get_data(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                       default: typing.Optional[str] = None) -> typing.Dict:
        return self._execute(chat, user)

    async def set_state(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                        state: typing.Optional[typing.AnyStr] = None):
        return self._execute(chat, user, data=state)

    async def set_data(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                       data: typing.Dict = None):
        return self._execute(chat, user, data=data)

    async def update_data(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                          data: typing.Dict = None,
                          **kwargs):
        return self._execute(chat, user, data=data)

    def has_bucket(self):
        return True

    async def get_bucket(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                         default: typing.Optional[dict] = None) -> typing.Dict:
        return self._execute(chat, user)

    async def set_bucket(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                         bucket: typing.Dict = None):
        return self._execute(chat, user, data=bucket)

    async def update_bucket(self, *, chat: typing.Union[str, int, None] = None,
                            user: typing.Union[str, int, None] = None, bucket: typing.Dict = None,
                            **kwargs):
        return self._execute(chat, user, data=bucket)

    @staticmethod
    async def get_states_list() -> typing.List[typing.Tuple[int, int]]:
        """
        Get list of all stored chat's and user's
        :return: list of tuples where first element is chat id and second is user id
        """
        result = []

        for _state in State().select():
            result.append((int(_state.chat), (int(_state.user))))

        return result

    def _execute(self, chat, user, data=None):
        chat, user = map(str, self.check_address(chat=chat, user=user))
        response = self._get_table_name_and_action(inspect.currentframe())

        if "get" == response["action"]:
            response = state_actions.action_get(self.bot_id, chat, user, response["column"])
        elif response["action"] in ["set", "update"]:
            response = state_actions.action_set(self.bot_id, chat, user, response["column"], data)
        return response

    @staticmethod
    def _get_table_name_and_action(current_frame):
        caller_frame = current_frame.f_back
        code_obj = caller_frame.f_code
        code_obj_name = str(code_obj.co_name)
        response = code_obj_name.split("_")
        if 2 == len(response):
            action = response[0]
            table_name = response[1]

            response = {
                "action": action,
                "column": table_name,
            }

        else:
            raise ValueError("Неожиданный ответ")

        return response

    @staticmethod
    async def reset_all():
        """
        Reset states in DB
        """
        return State().delete().execute()
