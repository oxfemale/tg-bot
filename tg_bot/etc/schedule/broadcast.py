import time
import asyncio

from aiogram.utils import exceptions


from ...config import bot
from ..text import messages
from tg_bot.etc.database import broadcast


async def broadcast_runner():
    broadcasts = broadcast.get_turned_off_broadcasts()
    if 0 < len(broadcasts):
        _broadcast = broadcasts[0]

        broadcast_result = {
            "success": 0,
            "bot_block": 0,
            "invalid_user_id": 0,
            "delete_account": 0,
            "telegram_errors": 0,
        }

        for recipient_chat_id in _broadcast.recipients:
            new_recipients_list = broadcast.profile(_broadcast.id).recipients.copy()
            new_recipients_list.remove(recipient_chat_id)

            broadcast.update_profile(_broadcast.id, "last_send", round(time.time()))
            broadcast.update_profile(_broadcast.id, "recipients", new_recipients_list)

            try:
                await bot.send_message(recipient_chat_id, _broadcast.text)
                broadcast_result["success"] += 1
                broadcast.update_profile(_broadcast.id, "success", broadcast.profile(_broadcast.id).success + 1)
            except exceptions.BotBlocked:
                broadcast_result["bot_block"] += 1
                broadcast.update_profile(_broadcast.id, "failed", broadcast.profile(_broadcast.id).failed + 1)
            except exceptions.ChatNotFound:
                broadcast_result["invalid_user_id"] += 1
                broadcast.update_profile(_broadcast.id, "failed", broadcast.profile(_broadcast.id).failed + 1)
            except exceptions.RetryAfter as e:
                await asyncio.sleep(e.timeout)
                return await bot.send_message(recipient_chat_id, text)
            except exceptions.UserDeactivated:
                broadcast_result["delete_account"] += 1
                broadcast.update_profile(_broadcast.id, "failed", broadcast.profile(_broadcast.id).failed + 1)
            except exceptions.TelegramAPIError:
                broadcast_result["telegram_errors"] += 1

        broadcast_result["unsuccessful"] = broadcast_result["bot_block"] + broadcast_result["delete_account"]

        mes = messages.broadcast_completed(_broadcast.id, broadcast_result)
        await bot.send_message(_broadcast.starter_chat_id, mes)
