from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Annotated, Optional, List, Union

from aiogram.types import User as AiogramUser


class User(BaseModel):
    id_user: int
    is_bot: Annotated[bool, Field(default=False)]
    first_name: str
    last_name: Annotated[Optional[str], Field(default=None)]
    username: Annotated[Optional[str], Field(default=None)]
    is_premium: Annotated[Optional[bool], Field(default=False)]
    is_active: Annotated[Optional[bool], Field(default=True)]
    language_code: str

    @classmethod
    def map_from_aiogram_user(
        cls,
        aiogram_user: AiogramUser,
    ) -> User:
        return User(
            id_user=aiogram_user.id,
            is_bot=aiogram_user.is_bot,
            first_name=aiogram_user.first_name,
            last_name=aiogram_user.last_name,
            username=aiogram_user.username,
            is_premium=aiogram_user.is_premium,
            language_code=aiogram_user.language_code,
            is_active=True,
        )


class UserList(BaseModel):
    id_user: List[str]