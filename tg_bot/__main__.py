import os
import aiogram

from . import filters
from . import handlers
from . import middlewares
from . import fsm_storage
from .etc.conf import settings
from .etc.database import models
from .etc import schedule as _schedule


def setup(filter=True, handler=False, middleware=True, schedule=False, use_django=False):
    settings.bot.parse_mode = aiogram.types.ParseMode.HTML
    settings.dispatcher.storage = fsm_storage.PeeweeORMStorage()
    models.create_tables()


    if filter:
        filters.setup(settings.dispatcher)

    if handler:
        handlers.setup(settings.dispatcher)

    if middleware:
        middlewares.setup(settings.dispatcher)

    if schedule:
        _schedule.setup()

    if use_django:
        import django
        django.setup()
