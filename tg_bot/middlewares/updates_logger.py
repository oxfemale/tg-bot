import aiogram


from ..config import dp
from ..etc.database import tg_bot_info


class UpdatesLogger(aiogram.dispatcher.middlewares.BaseMiddleware):
    def __init__(self):
        super(UpdatesLogger, self).__init__()

    @staticmethod
    async def on_post_process_message(_, __, ___: dict):
        tg_bot_info.update_data_amount_messages()

    @staticmethod
    async def on_post_process_callback_query(callback, __, ___: dict):
        tg_bot_info.update_data_amount_callbacks()

        try:
            await callback.answer("")
        except aiogram.utils.exceptions.InvalidQueryID:
            pass
