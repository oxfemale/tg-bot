from . import users
from .models import Admins
from tg_bot.etc.conf import settings


def get():
    admin_from_db = [users.profile(user_id=admin.user_id).chat_id for admin in Admins.select()]
    admins_list = settings.ADMINS_IDS + admin_from_db
    return admins_list


def check_user(chat_id=None, user_id=None):
    if chat_id:
        user_id = users.profile(chat_id=chat_id).id

    if Admins.get_or_none(user_id=user_id) or chat_id in settings.ADMINS_IDS:
        response = True
    else:
        response = False

    return response