from aiogram.fsm.context import FSMContext
from telegram_bot.api.server import Server
from telegram_bot.schema.user import User
from loguru import logger
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.filters import CommandObject
router = Router()


@router.message(CommandStart())
@logger.catch
async def start_handler(message: Message, server: Server, state: FSMContext, command: CommandObject):
    await state.clear()
    # if not await server.create_user(
    #         User.map_from_aiogram_user(
    #             aiogram_user=message.from_user,
    #         )
    # ):
    #
    #     # TODO: handle such cases properly
    #     logger.error("Can't create user", message.from_user)
    await message.answer("Привет")
