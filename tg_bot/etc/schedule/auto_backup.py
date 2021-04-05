import os
import sys
import time
import aiogram
import zipfile
import traceback

from tg_bot.etc.conf import settings
from tg_bot.etc.database import models
from tg_bot.etc.database import auto_backup as database_auto_backup


async def except_gasket(func):
    # keep_backup_minimum = settings.AUTO_BACKUP["keep_backup_minimum"]
    try:
        # time_left =  round(time.time()) < database_auto_backup.get_last_timestamp() +  keep_backup_minimum
        # if 0 < time_left:
        return await func()
    except Exception as _:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # print(type(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        # print(traceback.format_exception(exc_type, exc_value, exc_traceback))
        for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
            if line.endswith("\n"):
                line = line[:-1]
            print(line)


async def auto_backup_runner():
    backup_settings = settings.AUTO_BACKUP
    database_path = settings.DATABASE["name"]

    files_need_delete = []

    zip_path = os.path.join(settings.BASE_DIR.parent, "backup.zip")
    zip = zipfile.ZipFile(zip_path, "w")
    if backup_settings["database"]:
        zip.write(database_path, arcname=os.path.join("database", os.path.basename(database_path)))

    if backup_settings["sql_database"]:
        sql_file = os.path.join(settings.BASE_DIR.parent, "backup.sql")
        with open(sql_file, "w") as f:
            f.write(models.DataBase.import_sql())

        zip.write(sql_file, os.path.join("database", os.path.basename(sql_file)))

        files_need_delete.append(sql_file)

    if backup_settings["code"]:
        for root, dirs, files in os.walk("."):
            for _dir in ["__pycache__"]:
                if _dir in root:
                    break
            else:
                for file in files:
                    file_path = os.path.join(root, file)
                    zip.write(file_path, arcname=os.path.join("source", file_path))

    zip.close()

    file = aiogram.types.InputFile(zip_path)
    message = await settings.bot.send_document(backup_settings["chat_id"], file)
    files_need_delete.append(zip_path)
    for file in files_need_delete:
        os.remove(file)

    await database_auto_backup.write_new_backup(message.message_id)
