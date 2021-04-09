import peewee
import peewee_extra_fields

from tg_bot.etc.conf import settings
from tg_bot.etc.database import models, fields, validators


# noinspection PyUnusedLocal
def migrate(migrator, database, fake=False, **kwargs):
    class State(models.DataBase):
        bot_id = peewee.IntegerField(help_text="Идентефикатор бота")
        chat = peewee.TextField()
        user = peewee.TextField()
        state = peewee.TextField(null=True)
        data = peewee_extra_fields.JSONField(null=True)
        bucket = peewee_extra_fields.JSONField(null=True)

    State.create_table()

    class Broadcast(models.DataBase):
        starter_chat_id = peewee.IntegerField(help_text="Чай айди, кто запустил")
        text = peewee.TextField(help_text="Текст рассылки")
        recipients = peewee_extra_fields.JSONField(help_text="chat_id получателей")
        success = peewee.IntegerField(default=0, help_text="Кол-во юзеров успешно получили")
        failed = peewee.IntegerField(default=0, help_text="Кол-во юзеров не получили")
        last_send = peewee.TimestampField(default=0, help_text="Последнее отправленное сообщение")

    Broadcast.create_table()

    class CallbackDataFilter(models.DataBase):
        code = peewee.TextField(index=True, help_text="Код, который будет в callback_data")
        data = peewee_extra_fields.JSONField(help_text="Информация с кнопок")

    CallbackDataFilter.create_table()

    class AutoBackup(models.DataBase):
        backup_message_id = peewee.IntegerField(null=True, help_text="Айди сообщения с бекапом")
        timestamp = peewee.TimestampField(help_text="Время создания бекапа")

    AutoBackup.create_table()

    class TgBotBitcoinAddresses(models.DataBase):
        holder_chat_id = peewee.IntegerField(help_text="Айди владельца")
        address = peewee.TextField(unique=True, help_text="Адрес")
        address_id = peewee.TextField(unique=True, help_text="Айди адреса")
        using = peewee.BooleanField(default=False, help_text="Использован ли уже адрес")
        timestamp = peewee.TimestampField(help_text="Время создания")

    TgBotBitcoinAddresses.create_table()

    class TgBotSettings(models.DataBase):
        coinbase_api_key = peewee.IntegerField(null=True, help_text="Апи ключ коинбаз")
        coinbase_secret_key = peewee.IntegerField(null=True, help_text="Приват ключ коинбейза")
        fiat_currency = fields.TextField(validators=[validators.fiat_currency_validator], help_text="Валюта в боте")

    TgBotSettings.create_table()
    TgBotSettings.create(fiat_currency=settings.DEFAULT_FIAT_CURRENCY)

    class Admins(models.DataBase):
        user_id = peewee.IntegerField(help_text="Айди юзера")

    Admins.create_table()


# noinspection PyUnusedLocal
def rollback(migrator, database, fake=False, **kwargs):
    pass
