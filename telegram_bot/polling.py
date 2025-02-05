from telegram_bot.core.telegram import telegram_bot

from loguru import logger
from aiogram import Dispatcher


async def on_startup(dispatcher: Dispatcher):
    me = await telegram_bot.get_me()
    logger.info(f"Polling started for {me.first_name}@{me.username}")


async def on_shutdown(dispatcher: Dispatcher):
    logger.info("Polling shut down")


async def start_polling(dispatcher: Dispatcher):
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)
    await dispatcher.start_polling(telegram_bot)
