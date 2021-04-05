from ...config import dp


from aiogram import types
from aiogram.utils import exceptions


@dp.errors_handler(exception=exceptions.MessageNotModified)
async def message_not_modified(update: types.Update, error: exceptions.MessageNotModified):
	return True
