from typing import List
from .base import BaseServer
from loguru import logger
from telegram_bot.schema.lesson import Topic


class LessonAPI(BaseServer):

    @logger.catch
    async def list_topic(self) -> List[Topic] | None:
        response = await self.client.get(f"topics")
        if response.status_code != 200:
            return None
        topic_data = response.json()

        return [Topic(**topic) for topic in topic_data]
