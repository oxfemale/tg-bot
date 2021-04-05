from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tg_bot.etc.database import admins


class IsAdmin(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        if isinstance(message, types.CallbackQuery):
            message = message.message

        if self.is_admin == self.check_user_on_admin(message.chat.id):
            response = True
        else:
            response = False

        return response

    @staticmethod
    def check_user_on_admin(chat_id):
        return admins.check_user(chat_id=chat_id)
