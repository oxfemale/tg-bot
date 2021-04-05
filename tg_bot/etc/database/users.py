import time

from .models import Users
from tg_bot.etc.conf import settings


def get_user_model():
    return Users.get_model()


def get_all_chat_ids():
    return [user.chat_id for user in get_user_model().select()]


def profile(chat_id=None, user_id=None, bot_id=settings.BOT_ID):
    if chat_id:
        _profile = get_user_model().get_or_none(
            (get_user_model().chat_id == chat_id) & (get_user_model().bot_id == bot_id))
    elif user_id:
        _profile = Users().get_or_none(Users.id == user_id)

    # noinspection PyUnboundLocalVariable
    return _profile


def update(user_profile, table_name, value):
    setattr(user_profile, table_name, value)
    user_profile.save()


def get_amount_users():
    return Users.select().count()


def logger(chat_id, username, bot_id=settings.BOT_ID):
    _profile = profile(chat_id=chat_id, bot_id=bot_id)

    if _profile is None:
        _profile = new_user(chat_id, username, bot_id=bot_id)
    else:
        only = ["last_use"]
        if _profile.username != username:
            _profile.username = username
            only.append("username")

        _profile.last_use = time.time()
        _profile.save(only=only)

    return _profile


def new_user(chat_id, username, bot_id=settings.BOT_ID):
    return get_user_model().create(bot_id=bot_id, chat_id=chat_id, username=username)
