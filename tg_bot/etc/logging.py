import logging
from loguru import logger


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
    if logger_file is None:
        logging.basicConfig(handlers=[InterceptHandler()], level=logging_level)
    else:
        logger = logging.getLogger()
        logging_level = getattr(logging, logging_level)

        logger.setLevel(logging_level)
        handler = logging.FileHandler(logger_file, "w", encoding="UTF-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s"))
        logger.addHandler(handler)

