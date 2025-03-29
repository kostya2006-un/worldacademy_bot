from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.schema.lesson import Topic, Lesson
from telegram_bot.views.lesson import TRANSLATIONS


def topics_keyboard(
    topics: list[Topic],
    completed_topic_ids: set[int],
    available_topic_id: int,
    lang: str,
) -> InlineKeyboardMarkup:
    keyboard = []

    for topic in sorted(topics, key=lambda x: x.id):
        if topic.id <= available_topic_id:
            if topic.id in completed_topic_ids:
                text = TRANSLATIONS["completed_topic"][lang].format(title=topic.title)
            else:
                text = TRANSLATIONS["available_topic"][lang].format(title=topic.title)
            callback = f"topic_{topic.id}"
        else:
            text = TRANSLATIONS["locked_topic"][lang].format(title=topic.title)
            callback = "topic_locked"

        keyboard.append([InlineKeyboardButton(text=text, callback_data=callback)])

    keyboard.append(
        [
            InlineKeyboardButton(
                text=TRANSLATIONS["back"][lang], callback_data="main_menu"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def lessons_keyboard(
    lessons: list[Lesson],
    completed_lesson_ids: set[int],
    available_lesson_id: int,
    lang: str,
    topic_id: int,
) -> InlineKeyboardMarkup:
    keyboard = []

    for lesson in sorted(lessons, key=lambda x: x.id):
        if lesson.id <= available_lesson_id:
            if lesson.id in completed_lesson_ids:
                text = TRANSLATIONS["completed_lesson"][lang].format(title=lesson.title)
            else:
                text = TRANSLATIONS["available_lesson"][lang].format(title=lesson.title)
            callback = f"lesson_{topic_id}_{lesson.id}"
        else:
            text = TRANSLATIONS["locked_lesson"][lang].format(title=lesson.title)
            callback = "lesson_locked"

        keyboard.append([InlineKeyboardButton(text=text, callback_data=callback)])

    keyboard.append(
        [
            InlineKeyboardButton(
                text=TRANSLATIONS["back"][lang], callback_data=f"topic_{topic_id}_back"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def lesson_content_keyboard(
    topic_id: int, lesson_id: int, lang: str
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["start_test"][lang],
                    callback_data=f"test_{lesson_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["back"][lang],  # Кнопка назад к списку уроков
                    callback_data=f"topic_{topic_id}",
                )
            ],
        ]
    )


def lesson_test_keyboard(topic_id: int, lang: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["back_to_lessons"][lang],
                    callback_data=f"topic_{topic_id}",
                )
            ]
        ]
    )


def test_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TRANSLATIONS["back_to_lesson"][lang],
                    callback_data="back_to_lesson",
                )
            ]
        ]
    )
