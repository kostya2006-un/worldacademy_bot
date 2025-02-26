from aiogram.fsm.context import FSMContext
from telegram_bot.api.server import Server
from telegram_bot.schema.user import User
from loguru import logger
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from telegram_bot.keyboards.main_menu import main_menu_keyboard
from telegram_bot.views.start import TRANSLATIONS

router = Router()


@router.message(CommandStart())
@logger.catch
async def start_handler(message: Message, state: FSMContext, server: Server):
    await state.clear()
    await message.delete()
    user = await server.get_user_by_id(message.from_user.id)
    lang = user.language_code
    await message.answer(
        TRANSLATIONS["main_menu"][lang], reply_markup=main_menu_keyboard(lang)
    )
