from .start import router as start_router
from .settings import router as settings_router
from .utils import router as utils_router
from typing import Union
from aiogram import Dispatcher, Router


def include_routers(router: Union[Dispatcher | Router]):
    router.include_router(start_router)
    router.include_router(settings_router)
    router.include_router(utils_router)