from aiogram import Router
from aiogram.types import CallbackQuery
from telegram_bot.api.server import Server
from telegram_bot.keyboards.settings import (
    settings_keyboard,
    get_language_settings_keyboard,
    settings_back_keyboard,
)
from telegram_bot.views.settings import TRANSLATIONS

router = Router()


@router.callback_query(lambda c: c.data == "settings")
async def settings_handler(callback: CallbackQuery, server: Server):
    user = await server.get_user_by_id(callback.from_user.id)
    lang = user.language_code
    await callback.message.edit_text(
        TRANSLATIONS["settings_menu"][lang], reply_markup=settings_keyboard(lang)
    )


@router.callback_query(lambda c: c.data == "change_language")
async def settings_handler(callback: CallbackQuery, server: Server):
    user = await server.get_user_by_id(callback.from_user.id)
    lang = user.language_code
    await callback.message.edit_text(
        TRANSLATIONS["current_language"][lang],
        reply_markup=get_language_settings_keyboard(lang),
    )


@router.callback_query(lambda call: call.data.startswith("set_lang_"))
async def set_language_handler(call: CallbackQuery, server: Server):
    """Обработчик изменения языка."""
    new_language = call.data.split("_")[-1]
    user = await server.get_user_by_id(call.from_user.id)

    if user:
        user.language_code = new_language
        await server.put_user(user)

    await call.message.edit_text(
        TRANSLATIONS["language_changed"][new_language],
        reply_markup=settings_back_keyboard(new_language),
    )
