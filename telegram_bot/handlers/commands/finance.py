from aiogram import Router
from aiogram.types import CallbackQuery
from telegram_bot.api.server import Server
from telegram_bot.views.finance import TRANSLATIONS
from telegram_bot.keyboards.main_fin import main_finance_keyboard

router = Router()


@router.callback_query(lambda c: c.data == "portfolio")
async def finance_handler(callback: CallbackQuery, server: Server):
    user = await server.get_user_by_id(callback.from_user.id)
    lang = user.language_code
    portfolio = await server.get_my_finance(user.id_user)
    portfolio_value = await server.get_my_value(user.id_user)

    if not portfolio:
        await callback.message.answer(
            TRANSLATIONS["error"][lang],
        )
        return

    response_text = f"📈 {TRANSLATIONS['my_portfolio'][lang]}:\n\n"
    response_text += "\n".join(
        [
            f"🔹 {asset.ticker}: {asset.quantity} | (${asset.total_value})"
            for asset in portfolio
        ]
    )
    total_balance = portfolio_value.total_portfolio_value + user.balance
    percentage_change = round(((total_balance - 100000) / 100000) * 100, 2)
    response_text += f"\n🔹 USDT: {user.balance}"
    response_text += f"\n{TRANSLATIONS['final_portfolio'][lang]}: ${total_balance}"
    response_text += f"\n{TRANSLATIONS['percentage'][lang]}: {percentage_change}%"

    await callback.message.edit_text(
        response_text, reply_markup=main_finance_keyboard(lang)
    )


@router.callback_query(lambda c: c.data == "trade")
async def trading(callback: CallbackQuery, server: Server):
    await callback.message.edit_text("trade")
