import os
import peewee
import pathlib
from aiogram import Bot, Dispatcher

import config


BASE_DIR = pathlib.Path().resolve().parent
database = os.path.join(BASE_DIR, "db.sqlite3")


DATABASE = {
    "name": database,
    "peewee_engine": peewee.SqliteDatabase(database, thread_safe=True),
}


bot = Bot(token=config.MAIN_BOT_TOKEN)
dispatcher = Dispatcher(bot)


AUTO_BACKUP = {
    "code": True,  # Будет бекап всего архива
    "database": True,  #  Бекап базы данных файлом
    "sql_database": True,  # Бекап базы в sql
    "chat_id": -0,  # chat_id канала, лички и тд, куда будет отправляться бекап
    "interval": 60 * 60 * 24,  # Интервал в секундах между бекапами
    "last_backups_save": 10,  # Кол-во последних бекапов храниться. Последнии удаляются
    "keep_backup_minimum": 60 * 60 * 24 * 7,  # Мин время хранения бекапа. Далее удалиться
}