from typing import List
from .base import BaseServer
from loguru import logger
from telegram_bot.schema.finance import Portfolio, Value_Portfolio


class FinanceAPI(BaseServer):

    @logger.catch
    async def get_my_finance(self, user_id) -> List[Portfolio] | None:
        response = await self.client.get(f"finance/portfolio/{user_id}")
        if response.status_code != 200:
            return None
        fin_data = response.json()

        return [Portfolio(**asset) for asset in fin_data]

    @logger.catch
    async def get_my_value(self, user_id) -> Value_Portfolio | None:
        response = await self.client.get(f"finance/portfolio_value/{user_id}")
        if response.status_code != 200:
            return None
        return Value_Portfolio.model_validate(response.json())
