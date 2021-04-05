from ...config import dp


from aiogram import types
from aiogram.utils import exceptions


@dp.errors_handler(exception=exceptions.MessageToDeleteNotFound)
async def message_to_delete_not_found(update: types.Update, error: exceptions.MessageToDeleteNotFound):
    return True
