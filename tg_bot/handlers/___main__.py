from . import admin

from aiogram import Dispatcher


def setup(dispatcher: Dispatcher):
    admin.setup(dispatcher)
