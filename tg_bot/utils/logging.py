import os
import logging
from loguru import logger

from .. import config


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


def setup(logging_level="INFO", logger_file=None):
    if config.error_log is None and logger_file is None:
        logging.basicConfig(handlers=[InterceptHandler()], level=logging_level)
    else:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging_level)
        if os.path.exists(logger_file) is False:
            with open(logger_file, "w"):
                pass

        handler = logging.FileHandler(logger_file, "a", encoding="UTF-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s"))
        root_logger.addHandler(handler)
