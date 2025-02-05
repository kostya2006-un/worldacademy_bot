from telegram_bot.core.server import server
from telegram_bot.core.storage import storage
from telegram_bot.handlers.__main__ import register_handlers

from telegram_bot.logging import setup_logging
from telegram_bot.polling import start_polling

import asyncio
from aiogram import Dispatcher


def main():
    dispatcher = Dispatcher(storage=storage, server=server)
    register_handlers(dispatcher)

    asyncio.run(start_polling(dispatcher))


if __name__ == "__main__":
    setup_logging()
    main()
