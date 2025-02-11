from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot.views.start import TRANSLATIONS


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=TRANSLATIONS["articles"][lang], callback_data="articles")],
            [InlineKeyboardButton(text=TRANSLATIONS["qa"][lang], callback_data="qa")],
            [InlineKeyboardButton(text=TRANSLATIONS["portfolio"][lang], callback_data="portfolio")],
            [InlineKeyboardButton(text=TRANSLATIONS["ai_advisor"][lang], callback_data="ai_advisor")],
            #[InlineKeyboardButton(text=TRANSLATIONS["premium"][lang], callback_data="premium")],
            [InlineKeyboardButton(text=TRANSLATIONS["settings"][lang], callback_data="settings")],
        ]
    )

