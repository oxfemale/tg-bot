import os
from aiogram import types
from aiogram.dispatcher import FSMContext


from tg_bot.etc.database import users


async def load_user_for_tc(message: types.Message, _: FSMContext):
    with open("temp.txt") as f:
        for user_chat_id in users.get_all_chat_ids():
            f.write("{}\n".format(user_chat_id))

    file = types.InputFile("temp.txt")
    bot.send_document(message.chat.id, file)
    os.remove("temp.txt")
