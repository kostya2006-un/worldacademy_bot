from .start import router as start_router
from typing import Union
from aiogram import Dispatcher, Router


def include_routers(router: Union[Dispatcher | Router]):
    router.include_router(start_router)