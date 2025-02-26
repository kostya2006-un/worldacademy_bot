from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot.views.settings import TRANSLATIONS


def settings_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["change_language"][lang],
                    callback_data="change_language",
                )
            ],
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["back"][lang], callback_data="main_menu"
                )
            ],
        ]
    )


def get_language_settings_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Клавиатура для выбора языка и возврата в главное меню."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["languages"]["en"], callback_data="set_lang_en"
                )
            ],
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["languages"]["ru"], callback_data="set_lang_ru"
                )
            ],
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["back"][lang], callback_data="settings"
                )
            ],
        ]
    )


def settings_back_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["back"][lang], callback_data="settings"
                )
            ],
        ]
    )
