from .auth import AuthMiddleware

from typing import Union
from aiogram import Dispatcher, Router


def setup_middlewares(router: Union[Dispatcher, Router]):
    router.message.middleware(AuthMiddleware())
