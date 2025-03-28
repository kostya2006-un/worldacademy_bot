from datetime import datetime
from typing import List
from .base import BaseServer
from loguru import logger
from telegram_bot.schema.lesson import (
    Topic,
    UserCompletedTopic,
    Lesson,
    UserCompletedLesson,
    UserCompletedQuestion,
    Question,
    AnswerSchema,
)


class LessonAPI(BaseServer):

    @logger.catch
    async def list_topic(self) -> List[Topic] | None:
        response = await self.client.get(f"topics")
        if response.status_code != 200:
            return None
        topic_data = response.json()

        return [Topic(**topic) for topic in topic_data]

    @logger.catch
    async def get_completed_topics(
        self, user_id: int
    ) -> List[UserCompletedTopic] | None:
        response = await self.client.get(f"progress/topics/?user_id={user_id}")
        if response.status_code != 200:
            return None
        return [UserCompletedTopic(**topic) for topic in response.json()]

    @logger.catch
    async def get_lessons_by_topic(self, topic_id: int) -> List[Lesson] | None:
        response = await self.client.get(f"lessons/{topic_id}/")
        if response.status_code != 200:
            return None
        return [Lesson(**lesson) for lesson in response.json()]

    @logger.catch
    async def get_completed_lessons(
        self, user_id: int
    ) -> List[UserCompletedLesson] | None:
        response = await self.client.get(f"progress/lessons/?user_id={user_id}")
        if response.status_code != 200:
            return None
        return [UserCompletedLesson(**lesson) for lesson in response.json()]

    @logger.catch
    async def get_lesson(self, lesson_id: int):
        response = await self.client.get(f"lessons/detail/{lesson_id}/")
        return Lesson(**response.json()) if response.status_code == 200 else None

    @logger.catch
    async def get_questions_by_lesson(self, lesson_id: int):
        response = await self.client.get(f"questions/{lesson_id}/")
        return [Question(**q) for q in response.json()]

    @logger.catch
    async def get_completed_questions(self, user_id: int):
        response = await self.client.get(f"progress/questions/?user_id={user_id}")
        return [UserCompletedQuestion(**q) for q in response.json()]

    @logger.catch
    async def mark_question_completed(self, user_id: int, question_id: int) -> bool:
        """Отметить вопрос как пройденный"""
        data = UserCompletedQuestion(
            user_id=user_id, question_id=question_id
        ).model_dump()

        response = await self.client.post(
            "/progress/questions/", json=data  # Правильный эндпоинт
        )
        return response.status_code == 201

    @logger.catch
    async def mark_lesson_completed(self, user_id: int, lesson_id: int) -> bool:
        """Отметить урок как пройденный"""
        data = UserCompletedLesson(user_id=user_id, lesson_id=lesson_id).model_dump()

        response = await self.client.post("progress/lessons/", json=data)
        return response.status_code == 201

    @logger.catch
    async def mark_topic_completed(self, user_id: int, topic_id: int) -> bool:
        """Отметить тему как пройденную"""
        data = UserCompletedTopic(user_id=user_id, topic_id=topic_id).model_dump()

        response = await self.client.post("progress/topics/", json=data)
        return response.status_code == 201

    async def get_answers_by_question(self, question_id: int) -> List[AnswerSchema]:
        """Получить варианты ответов для вопроса"""
        response = await self.client.get(f"answers/{question_id}/")

        if response.status_code != 200:
            return []

        return [AnswerSchema(**answer_data) for answer_data in response.json()]
