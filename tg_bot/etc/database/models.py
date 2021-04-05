import peewee
import functools
import peewee_extra_fields

from . import fields
from . import validators
from ..conf import settings


def make_table_name(model):
    model_name = model.__name__
    pos = [i for i, e in enumerate(model_name + 'A') if e.isupper()]
    parts = [model_name[pos[j]:pos[j + 1]].lower() for j in range(len(pos) - 1)]
    table_name = "_".join(parts)
    return table_name


class DataBase(peewee.Model):
    CREATE_FIRST_RECORD = False

    class Meta:
        database = settings.DATABASE["peewee_engine"]
        table_function = make_table_name

    @classmethod
    def get_models(cls):
        return cls.__subclasses__()

    @classmethod
    def import_sql(cls):
        try:
            con = cls._meta.database.connect()
        except peewee.OperationalError:
            con = cls._meta.database.connection()

        sql = "\n".join(line for line in con.iterdump())

        return sql

    @classmethod
    def is_modified(cls):
        response = 0 < len(cls.__subclasses__())
        return response


class State(DataBase):
    bot_id = peewee.IntegerField(help_text="Идентефикатор бота")
    chat = peewee.TextField()
    user = peewee.TextField()
    state = peewee.TextField(null=True)
    data = peewee_extra_fields.JSONField(null=True)
    bucket = peewee_extra_fields.JSONField(null=True)


class TgBotInfo(DataBase):
    amount_messages = peewee.IntegerField(unique=True, default=0, help_text="Кол-во полученных сообщений")
    amount_callbacks = peewee.IntegerField(unique=True, default=0, help_text="Кол-во полученных каллбеков")
    amount_inlines = peewee.IntegerField(unique=True, default=0, help_text="Кол-во полученных инлайнов")

    CREATE_FIRST_RECORD = True


class Broadcast(DataBase):
    starter_chat_id = peewee.IntegerField(help_text="Чай айди, кто запустил")
    text = peewee.TextField(help_text="Текст рассылки")
    recipients = peewee_extra_fields.JSONField(help_text="chat_id получателей")
    success = peewee.IntegerField(default=0, help_text="Кол-во юзеров успешно получили")
    failed = peewee.IntegerField(default=0, help_text="Кол-во юзеров не получили")
    last_send = peewee.TimestampField(default=0, help_text="Последнее отправленное сообщение")


class CallbackDataFilter(DataBase):
    code = peewee.TextField(index=True, help_text="Код, который будет в callback_data")
    data = peewee_extra_fields.JSONField(help_text="Информация с кнопок")


class AutoBackup(DataBase):
    backup_message_id = peewee.IntegerField(null=True, help_text="Айди сообщения с бекапом")
    timestamp = peewee.TimestampField(help_text="Время создания бекапа")


class TgBotBitcoinAddresses(DataBase):
    holder_chat_id = peewee.IntegerField(help_text="Айди владельца")
    address = peewee.TextField(unique=True, help_text="Адрес")
    address_id = peewee.TextField(unique=True, help_text="Айди адреса")
    using = peewee.BooleanField(default=False, help_text="Использован ли уже адрес")
    timestamp = peewee.TimestampField(help_text="Время создания")


class TgBotSettings(DataBase):
    coinbase_api_key = peewee.IntegerField(null=True, help_text="Апи ключ коинбаз")
    coinbase_secret_key = peewee.IntegerField(null=True, help_text="Приват ключ коинбейза")
    fiat_currency = fields.TextField(
        default=settings.DEFAULT_FIAT_CURRENCY,
        validators=[validators.fiat_currency_validator],
        help_text="Валюта в боте")

    CREATE_FIRST_RECORD = True


class Admins(DataBase):
    user_id = peewee.IntegerField(help_text="Айди юзера")


class Users(DataBase):
    bot_id = peewee.IntegerField(help_text="Айди бота, в котором юзер")
    chat_id = peewee.IntegerField(help_text="Чат айди юзера")
    username = peewee.TextField(null=True, help_text="Юзернейм юзера")
    reg_time = peewee.TimestampField(help_text="Дата регистрации")
    last_use = peewee.TimestampField(help_text="Последние использование")

    @classmethod
    @functools.lru_cache()
    def get_modified_model(cls):
        return cls.__subclasses__()[0]

    @classmethod
    @functools.lru_cache()
    def get_model(cls):
        if 0 < len(cls.__subclasses__()):
            user_model = cls.__subclasses__()[0]
        else:
            user_model = cls

        return user_model


def create_tables():
    for model in DataBase().get_models():
        if model.table_exists() is False and model.is_modified() is False:
            model.create_table()

            if model.CREATE_FIRST_RECORD:
                model.create()
