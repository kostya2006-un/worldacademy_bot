from telegram_bot.core.settings import Settings

import redis.asyncio as redis
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage

if redis_uri := Settings().redis_uri:
    storage = MemoryStorage()

    # I'm really not proud of this :c solve your serialisation!! TODO TODO TODO
    # storage = RedisStorage(redis.from_url(redis_uri))
else:
    storage = MemoryStorage()
