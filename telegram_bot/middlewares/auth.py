from telegram_bot.core.settings import Settings
from telegram_bot.schema.user import User
from telegram_bot.api.server import Server
from typing import Dict
from aiogram import BaseMiddleware, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Update, Message, CallbackQuery

from loguru import logger

settings = Settings()


class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, update: Update, data: Dict):
        if type(update) not in [Message, CallbackQuery]:
            logger.error(f"Unknown event {update=}")
            return

        telegram_user = update.from_user
        server: Server = data.get("server")
        bot: Bot = data.get("bot")

        user = await server.get_user_by_id(telegram_user.id)

        if not user:
            # Если пользователя нет в БД, создаем его
            user = await server.create_user(
                User.map_from_aiogram_user(aiogram_user=telegram_user)
            )

        return await handler(update, {**data, "user": user})