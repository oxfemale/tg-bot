from aiogram import Dispatcher

from .text import load_user_for_tc



def setup(dispatcher: Dispatcher):
    dispatcher.register_message_handler(load_user_for_tc, text="Выгрузить список юзеров для TC", state=None)
