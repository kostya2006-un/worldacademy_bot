from loguru import logger
from telegram_bot.core.settings import Settings

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.utils.token import TokenValidationError


try:
    telegram_bot = Bot(Settings().telegram_token)
except TokenValidationError:
    logger.critical("Token is invalid")
    exit(1)
