import time
import traceback

from aiogram import types
from aiogram.utils import exceptions


from ...config import dp, ADMINS_IDS


@dp.errors_handler(lambda exception: exception not in 
                   [exceptions.MessageNotModified, exceptions.MessageToDeleteNotFound]
                   )
async def other_exceptions(update: types.Update, error: Exception):
    error_text = traceback.format_exc()

    text = "<b>Текст ошибки:</b>\n <code>{}</code>\n <b>Update:</b>\n <code>{}</code>"
    text = text.format(error_text, update)

    chat_id = ADMINS_IDS[0]

    await bot.send_message(chat_id, text)
    return True
