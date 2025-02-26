from aiogram import Router
from aiogram.types import CallbackQuery
from telegram_bot.api.server import Server
from telegram_bot.keyboards.main_menu import main_menu_keyboard
from telegram_bot.views.start import TRANSLATIONS

router = Router()


@router.callback_query(lambda c: c.data == "main_menu")
async def settings_handler(callback: CallbackQuery, server: Server):
    user = await server.get_user_by_id(callback.from_user.id)
    lang = user.language_code
    await callback.message.edit_text(
        TRANSLATIONS["main_menu"][lang], reply_markup=main_menu_keyboard(lang)
    )
