from datetime import datetime

from pydantic import BaseModel, field_serializer


class Topic(BaseModel):
    title: str
    id: int


class UserCompletedTopic(BaseModel):
    user_id: int
    topic_id: int


class Lesson(BaseModel):
    id: int
    topic_id: int
    title: str
    content: str


class UserCompletedLesson(BaseModel):
    user_id: int
    lesson_id: int


class UserCompletedQuestion(BaseModel):
    user_id: int
    question_id: int
    completed_at: datetime = datetime.now()

    @field_serializer("completed_at")
    def serialize_dt(self, dt: datetime) -> str:
        return dt.isoformat()


class Question(BaseModel):
    id: int
    lesson_id: int
    question_text: str


class AnswerSchema(BaseModel):
    id: int
    question_id: int
    answer_text: str
    is_correct: bool
