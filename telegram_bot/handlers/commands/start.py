from aiogram.fsm.context import FSMContext
from telegram_bot.api.server import Server
from telegram_bot.schema.user import User
from loguru import logger
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.filters import CommandObject
router = Router()


@router.message(CommandStart())
@logger.catch
async def start_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Привет!")
