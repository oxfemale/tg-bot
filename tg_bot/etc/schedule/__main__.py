import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from . import broadcast
from . import auto_backup
from tg_bot.etc.conf import settings


def setup(broadcast_runner=False):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    scheduler = AsyncIOScheduler(loop=loop)
    if broadcast_runner:
        scheduler.add_job(broadcast.broadcast_runner, "interval", minutes=1)
    if True in [settings.AUTO_BACKUP["database"], settings.AUTO_BACKUP["code"], settings.AUTO_BACKUP["sql_database"]]:
        args = [auto_backup.auto_backup_runner]
        interval = settings.AUTO_BACKUP["interval"]
        scheduler.add_job(auto_backup.except_gasket, trigger="interval", args=args, seconds=interval)

    scheduler.start()
