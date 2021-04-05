import os
import shutil

from . import tests
from . import BaseCommand
from tg_bot.etc.conf import settings


class Command(BaseCommand):
    def handle(self):
        base_dir = settings.BASE_DIR
        htmlcov_dir = os.path.join(base_dir.parent, "htmlcov")

        tests.Command().delete_test_db_if_exists_and_drop_tables()
        os.system("pytest -s --cov=../src/ ../tests/")
        os.system("coverage html")

        if os.path.exists(htmlcov_dir):
            shutil.rmtree(htmlcov_dir)

        shutil.move(os.path.join(base_dir, "htmlcov"), htmlcov_dir)
