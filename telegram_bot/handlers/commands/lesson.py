from aiogram import Router
from aiogram.types import CallbackQuery
from telegram_bot.api.server import Server
from telegram_bot.keyboards.lesson import topics_keyboard
from telegram_bot.views.lesson import TRANSLATIONS

router = Router()


@router.callback_query(lambda c: c.data == "articles")
async def art_handler(callback: CallbackQuery, server: Server):
    user = await server.get_user_by_id(callback.from_user.id)
    lang = user.language_code
    topics = await server.list_topic()

    await callback.message.edit_text(
        text=TRANSLATIONS["choose_topic"][lang],
        reply_markup=topics_keyboard(topics=topics, lang=lang),
    )
