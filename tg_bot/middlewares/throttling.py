import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler


from ..config import dp
from ..filters import is_admin


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, _: dict):
        if await is_admin.IsAdmin(False).check(message):
            dispatcher = Dispatcher.get_current()
            limit = self.rate_limit
            key = f"{self.prefix}_message"
            try:
                await dispatcher.throttle(key, rate=limit)
            except Throttled as t:
                await self.message_throttled(message, t)
                raise CancelHandler()

    @staticmethod
    async def message_throttled(_: types.Message, throttled: Throttled):
        delta = throttled.rate - throttled.delta
        await asyncio.sleep(delta)
