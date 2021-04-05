import aiogram

from tg_bot.etc.conf import settings
from tg_bot.etc.database import users


class UsersLogger(aiogram.dispatcher.middlewares.BaseMiddleware):
    def __init__(self, bot_id=settings.BOT_ID, logger=users.logger):
        self.bot_id = bot_id
        self._logger = logger
        super(UsersLogger, self).__init__()

    async def on_pre_process_message(self, message: aiogram.types.Message, _: dict):
        self.logger(message)

    async def on_pre_process_callback_query(self, callback: aiogram.types.CallbackQuery, _: dict):
        self.logger(callback.message)

    def logger(self, message: aiogram.types.Message):
        user = self._logger(message.chat.id, message.chat.username, bot_id=self.bot_id)
        setattr(message, "user", user)
