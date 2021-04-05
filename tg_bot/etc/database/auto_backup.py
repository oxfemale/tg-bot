import time
import aiogram

from .models import AutoBackup
from tg_bot.etc.conf import settings

backup_settings = settings.AUTO_BACKUP


async def write_new_backup(message_id):
    if backup_settings["last_backups_save"] <= get_amount_backups():
        keep_backup_minimum = backup_settings["keep_backup_minimum"]
        for backup in AutoBackup.select().where((AutoBackup.timestamp + keep_backup_minimum) <= time.time()):
            try:
                await settings.bot.delete_message(backup_settings["channel_chat_id"], backup.backup_message_id)
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass

            AutoBackup.delete().where(AutoBackup.id == backup.id).execute()

            if backup_settings["last_backups_save"] > get_amount_backups():
                break

    AutoBackup.create(backup_message_id=message_id)


def get_last_timestamp():
    record = AutoBackup.select().order_by(AutoBackup.id.desc(nulls="LAST"))
    if record is not None:
        last_timestamp = record.timestamp
    else:
        last_timestamp = 0
    return last_timestamp


def get_amount_backups():
    return AutoBackup.select().count()
