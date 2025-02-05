import inspect
from loguru import logger

import logging
from logging import Handler, LogRecord


class InterceptHandler(Handler):

    def emit(self, record: LogRecord):

        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0

        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging():

    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("aiogram")
    )

    for logger_ in loggers:
        logger_.handlers = [InterceptHandler()]
