from aiogram import Dispatcher

from . import i18n
from . import throttling
from . import users_logger
from ..etc.conf import settings


def setup(dp: Dispatcher, user_logger=None, user_profile=None, i18nmiddleware=False):
    dp.middleware.setup(users_logger.UsersLogger())
    dp.middleware.setup(throttling.ThrottlingMiddleware())

    if i18nmiddleware:
        settings.i18n = i18n.I18nMiddleware(user_profile)
        dp.middleware.setup(settings.i18n)
