from telegram_bot.handlers.commands.__main__ import (
    include_routers as include_command_routers,
)


from telegram_bot.handlers.onboarding.__main__ import (
    include_routers as include_onboarding_routers,
)

from aiogram import Dispatcher, Router
from telegram_bot.middlewares.__main__ import setup_middlewares


def register_handlers(dispatcher: Dispatcher):
    router = Router()
    setup_middlewares(router)

    include_command_routers(router)
    include_onboarding_routers(router)

    dispatcher.include_router(router)
