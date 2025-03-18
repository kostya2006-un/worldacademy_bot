from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot.views.lesson import TRANSLATIONS


def topics_keyboard(topics: list, lang: str) -> InlineKeyboardMarkup:
    """
    Генерирует клавиатуру со списком тем и кнопкой "Назад"
    :param topics: Список объектов Topic
    :param lang: Язык пользователя
    :return: Объект инлайн-клавиатуры
    """
    keyboard = []

    # Добавляем кнопки тем
    for topic in topics:
        keyboard.append(
            [InlineKeyboardButton(text=topic.title, callback_data=f"topic_{topic.id}")]
        )

    # Добавляем кнопку "Назад"
    keyboard.append(
        [
            InlineKeyboardButton(
                text=TRANSLATIONS["back"][lang], callback_data="main_menu"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
