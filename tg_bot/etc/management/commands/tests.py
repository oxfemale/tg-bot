import os
import pytest
import peewee
import peewee_migrate

from . import BaseCommand
from tg_bot.etc.conf import settings
from tg_bot.etc.database import models


class Command(BaseCommand):
    def delete_test_db_if_exists_and_drop_tables(self):
        if os.path.exists("test.db"):
            os.unlink("test.db")

        self.drop_tables()  # Чистка таблиц и миграция

    def handle(self):
        os.system("pytest ../tests -s")

    @staticmethod
    def drop_tables():
        database_engine = models.DataBase._meta.database

        # !!!!! When there is an inheritance from the model to tg_bot, it will delete
        from classes.database.models import DataBase
        _models = DataBase.get_models()

        DataBase._meta.database.init("test.db")
        models.DataBase._meta.database.init("test.db")

        peewee_migrate.MigrateHistory._meta.database = models.DataBase._meta.database
        peewee_migrate.MigrateHistory._meta.database.init("test.db")


        for model in models.DataBase.get_models() + [peewee_migrate.MigrateHistory] + _models:
            if model.table_exists():
                model.drop_table(safe=False)



        # This will be cut out later, when I stop using the sql file for tables!!!
        import run
        sql_file_path = os.path.join(settings.BASE_DIR, "etc/data/bases/database.sql")
        if os.path.exists(sql_file_path):
            with open(sql_file_path, encoding="utf-8") as f:
                sql = f.read()

            run.create_db("test.db", sql)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        migrate_dir = os.path.join(settings.BASE_DIR, "etc/migrations")
        router = peewee_migrate.Router(models.DataBase._meta.database, migrate_dir=migrate_dir)
        router.logger.disabled = True
        router.run()
