from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, PollAnswer
from aiogram.fsm.context import FSMContext
from loguru import logger

from telegram_bot.api.server import Server
from telegram_bot.keyboards.lesson import (
    topics_keyboard,
    lessons_keyboard,
    lesson_content_keyboard,
    lesson_test_keyboard,
)
from telegram_bot.schema.lesson import (
    UserCompletedQuestion,
    UserCompletedLesson,
    UserCompletedTopic,
)
from telegram_bot.views.lesson import TRANSLATIONS
from telegram_bot.state.onboarding import TestStates

router = Router()


# Хендлеры для тем
@router.callback_query(lambda c: c.data == "articles")
async def art_handler(callback: CallbackQuery, server: Server):
    user = await server.get_user_by_id(callback.from_user.id)
    lang = user.language_code

    topics = await server.list_topic()
    if not topics:
        await callback.message.edit_text(text=TRANSLATIONS["no_topics_available"][lang])
        return

    completed_topics = await server.get_completed_topics(user.id_user)
    completed_ids = (
        {topic.topic_id for topic in completed_topics} if completed_topics else set()
    )

    max_completed = max(completed_ids) if completed_ids else 0
    available_topic_id = max_completed + 1 if completed_ids else 1

    await callback.message.edit_text(
        text=TRANSLATIONS["choose_topic"][lang],
        reply_markup=topics_keyboard(
            topics=topics,
            completed_topic_ids=completed_ids,
            available_topic_id=available_topic_id,
            lang=lang,
        ),
    )


@router.callback_query(lambda c: c.data == "topic_locked")
async def handle_locked_topic(callback: CallbackQuery, server: Server):
    user = await server.get_user_by_id(callback.from_user.id)
    await callback.answer(
        TRANSLATIONS["topic_locked"][user.language_code], show_alert=True
    )


@router.callback_query(lambda c: c.data.startswith("topic_"))
async def topic_handler(callback: CallbackQuery, server: Server):
    if "_back" in callback.data:
        return await art_handler(callback, server)

    topic_id = int(callback.data.split("_")[1])
    user = await server.get_user_by_id(callback.from_user.id)
    lang = user.language_code

    lessons = await server.get_lessons_by_topic(topic_id)
    if not lessons:
        await callback.message.edit_text(TRANSLATIONS["no_lessons_available"][lang])
        return

    completed_lessons = await server.get_completed_lessons(user.id_user)
    completed_ids = {l.lesson_id for l in completed_lessons}

    max_completed = max(completed_ids) if completed_ids else 0
    available_lesson_id = max_completed + 1 if completed_ids else 1

    await callback.message.edit_text(
        text=TRANSLATIONS["choose_lesson"][lang],
        reply_markup=lessons_keyboard(
            lessons=lessons,
            completed_lesson_ids=completed_ids,
            available_lesson_id=available_lesson_id,
            lang=lang,
            topic_id=topic_id,
        ),
    )


# Хендлеры для уроков
@router.callback_query(lambda c: c.data == "lesson_locked")
async def handle_locked_lesson(callback: CallbackQuery, server: Server):
    user = await server.get_user_by_id(callback.from_user.id)
    await callback.answer(
        TRANSLATIONS["lesson_locked"][user.language_code], show_alert=True
    )


@router.callback_query(lambda c: c.data.startswith("lesson_"))
async def lesson_handler(callback: CallbackQuery, server: Server):
    _, topic_id, lesson_id = callback.data.split("_")
    topic_id = int(topic_id)
    lesson_id = int(lesson_id)

    user = await server.get_user_by_id(callback.from_user.id)
    lang = user.language_code

    lesson = await server.get_lesson(lesson_id)

    await callback.message.edit_text(
        text=f"📖 {lesson.title}\n\n{lesson.content}",
        reply_markup=lesson_content_keyboard(
            topic_id=topic_id, lesson_id=lesson_id, lang=lang
        ),
    )


# Хендлеры для тестов
@router.callback_query(F.data.startswith("test_"))
async def start_test_handler(
    callback: CallbackQuery, state: FSMContext, server: Server
):
    lesson_id = int(callback.data.split("_")[1])
    user = await server.get_user_by_id(callback.from_user.id)
    # Сначала получаем урок, чтобы получить topic_id
    lesson = await server.get_lesson(lesson_id)
    if not lesson:
        await callback.answer("Урок не найден!")
        return

    questions = await server.get_questions_by_lesson(lesson_id)
    completed = await server.get_completed_questions(user.id_user)

    unanswered = [
        q for q in questions if q.id not in {c.question_id for c in completed}
    ]

    if not unanswered:
        await callback.answer(
            TRANSLATIONS["test_already_completed"][user.language_code]
        )
        return

    await state.update_data(
        message=callback.message,
        current_question=0,
        questions=unanswered,
        lesson_id=lesson_id,
        topic_id=lesson.topic_id,  # Теперь получаем topic_id из урока
    )

    await state.set_state(TestStates.in_test)
    await send_next_question(state, server)


async def send_next_question(state: FSMContext, server: Server):
    data = await state.get_data()
    question = data["questions"][data["current_question"]]
    message = data["message"]

    try:
        # Получаем ответы и проверяем их наличие
        answers = await server.get_answers_by_question(question.id)
        if not answers:
            await message.answer("🚫 Для этого вопроса нет ответов")
            await state.clear()
            return

        # Проверяем наличие правильного ответа
        correct_options = [i for i, a in enumerate(answers) if a.is_correct]
        if not correct_options:
            await message.answer("🚫 В вопросе нет правильного ответа")
            await state.clear()
            return

        # Отправляем опрос
        await message.bot.send_poll(
            chat_id=message.chat.id,
            question=question.question_text,
            options=[a.answer_text for a in answers],
            type="quiz",
            correct_option_id=correct_options[0],
            is_anonymous=False,
            explanation=(
                "Продолжайте тест!"
                if data["current_question"] + 1 < len(data["questions"])
                else "Тест завершен!"
            ),
        )

    except Exception as e:
        logger.error(f"Ошибка отправки вопроса: {str(e)}")
        await state.clear()


@router.poll_answer(TestStates.in_test)
async def handle_poll_answer(
    poll_answer: PollAnswer, state: FSMContext, server: Server
):
    try:
        data = await state.get_data()
        user_id = poll_answer.user.id
        current_idx = data["current_question"]
        question = data["questions"][current_idx]

        # Проверка правильности ответа
        answers = await server.get_answers_by_question(question.id)
        correct_option = next((i for i, a in enumerate(answers) if a.is_correct), None)

        if correct_option is None:
            await state.clear()
            return

        # Если ответ неправильный - повторяем вопрос
        if poll_answer.option_ids[0] != correct_option:
            await send_next_question(state, server)
            return

        # Отмечаем вопрос как пройденный
        await server.mark_question_completed(user_id, question.id)

        # Проверяем, все ли вопросы урока пройдены
        completed_questions = await server.get_completed_questions(user_id)
        all_questions = await server.get_questions_by_lesson(data["lesson_id"])
        completed_question_ids = {q.question_id for q in completed_questions}

        if all(q.id in completed_question_ids for q in all_questions):
            await server.mark_lesson_completed(user_id, data["lesson_id"])

            # Проверяем, все ли уроки темы пройдены
            lessons = await server.get_lessons_by_topic(data["topic_id"])
            completed_lessons = await server.get_completed_lessons(user_id)
            completed_lesson_ids = {l.lesson_id for l in completed_lessons}

            if all(lesson.id in completed_lesson_ids for lesson in lessons):
                await server.mark_topic_completed(user_id, data["topic_id"])

            # Отправляем пользователя в меню выбора урока
            await state.clear()
            await poll_answer.user.send_message(
                "✅ Урок завершен! Выберите следующий урок:",
                reply_markup=await lessons_keyboard(data["topic_id"], server),
            )
            return

        # Переход к следующему вопросу или завершение
        if current_idx + 1 >= len(data["questions"]):
            await state.clear()
            await send_test_completion_message(user_id, data["lesson_id"], server)
        else:
            await state.update_data(current_question=current_idx + 1)
            await send_next_question(state, server)

    except Exception as e:
        logger.error(f"Ошибка обработки: {str(e)}")
        await state.clear()


async def send_test_completion_message(user_id: int, lesson_id: int, server: Server):
    lesson = await server.get_lesson(lesson_id)
    user = await server.get_user_by_id(user_id)
    lang = user.language_code

    # await server.bot.send_message(
    #     chat_id=user_id,
    #     text=TRANSLATIONS["test_completed"].get(lang, "🎉 Тест завершен!"),
    #     reply_markup=lesson_test_keyboard(lesson.topic_id, lang),
    # )
