from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from telegram_bot.api.server import Server
from telegram_bot.schema.finance import Trade
from telegram_bot.state.onboarding import OnboardingState
from telegram_bot.views.finance import TRANSLATIONS
from telegram_bot.keyboards.main_fin import (
    main_finance_keyboard,
    trading_keyboard,
    back_trade_fin,
)

router = Router()


@router.callback_query(lambda c: c.data == "portfolio")
async def finance_handler(callback: CallbackQuery, server: Server, state: FSMContext):
    await state.clear()
    user = await server.get_user_by_id(callback.from_user.id)
    lang = user.language_code
    portfolio = await server.get_my_finance(user.id_user)
    portfolio_value = await server.get_my_value(user.id_user)

    if not portfolio:
        await callback.message.answer(TRANSLATIONS["error"][lang])
        return

    response_text = f"📈 {TRANSLATIONS['my_portfolio'][lang]}:\n\n"
    response_text += "\n".join(
        [
            f"🔹 {asset.ticker}: {asset.quantity} | (${asset.total_value})"
            for asset in portfolio
        ]
    )
    total_balance = round(portfolio_value.total_portfolio_value + user.balance, 2)
    percentage_change = round(((total_balance - 100000) / 100000) * 100, 2)
    response_text += f"\n🔹 USDT: {user.balance}"
    response_text += f"\n{TRANSLATIONS['final_portfolio'][lang]}: ${total_balance}"
    response_text += f"\n{TRANSLATIONS['percentage'][lang]}: {percentage_change}%"

    await callback.message.edit_text(
        response_text, reply_markup=main_finance_keyboard(lang)
    )


@router.callback_query(lambda c: c.data == "trade")
async def trading(callback: CallbackQuery, server: Server):
    user = await server.get_user_by_id(callback.from_user.id)
    lang = user.language_code
    assets = await server.get_assets()
    portfolio = await server.get_my_finance(user.id_user)

    if not assets:
        await callback.message.answer(TRANSLATIONS["error"][lang])
        return

    asset_index = 0
    asset = assets[asset_index]
    asset_quantity = next(
        (p.quantity for p in portfolio if p.ticker == asset.ticker), 0
    )

    text = (
        f"{asset.name} ({asset.ticker})\n"
        f"💰 {TRANSLATIONS['fin_buy'][lang]}: ${asset.price}\n"
        f"👤 {TRANSLATIONS['my_portfolio'][lang]}: ${user.balance}\n"
        f"📊 {TRANSLATIONS['my_portfolio'][lang]}: {asset_quantity} {asset.ticker}"
    )

    await callback.message.edit_text(
        text, reply_markup=trading_keyboard(asset, asset_index, lang)
    )


@router.callback_query(lambda c: c.data.startswith("trade_nav:"))
async def trade_navigation(callback: CallbackQuery, server: Server):
    user = await server.get_user_by_id(callback.from_user.id)
    lang = user.language_code
    assets = await server.get_assets()
    portfolio = await server.get_my_finance(user.id_user)
    asset_index = int(callback.data.split(":")[1])

    if asset_index < 0:
        asset_index = len(assets) - 1
    elif asset_index >= len(assets):
        asset_index = 0

    asset = assets[asset_index]
    asset_quantity = next(
        (p.quantity for p in portfolio if p.ticker == asset.ticker), 0
    )

    text = (
        f"{asset.name} ({asset.ticker})\n"
        f"💰 {TRANSLATIONS['fin_buy'][lang]}: ${asset.price}\n"
        f"👤 {TRANSLATIONS['my_portfolio'][lang]}: ${user.balance}\n"
        f"📊 {TRANSLATIONS['my_portfolio'][lang]}: {asset_quantity} {asset.ticker}"
    )

    await callback.message.edit_text(
        text, reply_markup=trading_keyboard(asset, asset_index, lang)
    )


@router.callback_query(lambda c: c.data.startswith("trade_buy"))
async def trade_buy(callback: CallbackQuery, state: FSMContext, server: Server):
    data = callback.data.split(":")  # trade_buy:{ticker}:{price}
    ticker, price = data[1], float(data[2])

    user = await server.get_user_by_id(callback.from_user.id)
    lang = user.language_code
    portfolio = await server.get_my_finance(user.id_user)
    asset_quantity = next((p.quantity for p in portfolio if p.ticker == ticker), 0)

    await state.update_data(ticker=ticker, price=price)

    text = (
        f"{ticker}\n"
        f"💰 {TRANSLATIONS['fin_buy'][lang]}: ${price}\n"
        f"👤 {TRANSLATIONS['my_portfolio'][lang]}: ${user.balance}\n"
        f"📊 {TRANSLATIONS['my_portfolio'][lang]}: {asset_quantity} {ticker}\n\n"
        f"{TRANSLATIONS['enter_amount'][lang]}"
    )

    await callback.message.edit_text(text, reply_markup=back_trade_fin(lang))
    await state.set_state(OnboardingState.amount)


@router.message(OnboardingState.amount)
async def process_buy_amount(message: Message, state: FSMContext, server: Server):
    user = await server.get_user_by_id(message.from_user.id)
    lang = user.language_code
    data = await state.get_data()
    ticker, price = data["ticker"], data["price"]

    try:
        amount_to_invest = float(message.text)
        if amount_to_invest <= 0:
            raise ValueError
    except ValueError:
        await message.answer(TRANSLATIONS["invalid_amount"][lang])
        return

    if amount_to_invest > user.balance:
        await message.answer(TRANSLATIONS["insufficient_funds"][lang])
        return

    quantity_to_buy = amount_to_invest / price

    # Создаём объект Trade с помощью нового метода create()
    trade = Trade.create_trade(
        user_id=user.id_user, ticker=ticker, trade_type="buy", quantity=quantity_to_buy
    )

    user = await server.get_user_by_id(message.from_user.id)
    portfolio = await server.get_my_finance(user.id_user)
    asset_quantity = next((p.quantity for p in portfolio if p.ticker == ticker), 0)

    assets = await server.get_assets()
    asset = next((a for a in assets if a.ticker == ticker), None)

    if not asset:
        await message.answer(TRANSLATIONS["asset_not_found"][lang])
        return

    text = TRANSLATIONS["buy_success"][lang].format(
        quantity=quantity_to_buy, ticker=ticker
    )

    await message.answer(
        text, reply_markup=trading_keyboard(asset, 0, user.language_code)
    )
    await state.clear()


@router.callback_query(lambda c: c.data.startswith("trade_sell"))
async def trade_sell(callback: CallbackQuery):
    await callback.answer("Продажа в разработке 🛠")
