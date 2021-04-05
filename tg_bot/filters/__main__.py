from aiogram import Dispatcher

from . import is_admin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(is_admin.IsAdmin)
