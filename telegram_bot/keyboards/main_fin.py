from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.schema.asset import Asset
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


def trading_keyboard(asset: Asset, asset_index: int, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⏪", callback_data=f"trade_nav:{asset_index-1}"
                ),
                InlineKeyboardButton(
                    text="Купить",
                    callback_data=f"trade_buy:{asset.ticker}:{asset.price}",
                ),
                InlineKeyboardButton(
                    text=TRANSLATIONS["fin_sell"][lang],
                    callback_data=f"trade_sell:{asset.ticker}:{asset.price}",
                ),
                InlineKeyboardButton(
                    text="⏩", callback_data=f"trade_nav:{asset_index+1}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["back"][lang], callback_data="portfolio"
                )
            ],
        ]
    )


def back_trade_fin(lang: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["back"][lang], callback_data="portfolio"
                )
            ],
        ]
    )
