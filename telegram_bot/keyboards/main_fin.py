from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot.views.finance import TRANSLATIONS


def main_finance_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["trade"][lang], callback_data="trade"
                )
            ],
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["back"][lang], callback_data="main_menu"
                )
            ],
        ]
    )
