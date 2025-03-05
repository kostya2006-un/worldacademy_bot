from typing import List
from .base import BaseServer
from loguru import logger
from telegram_bot.schema.finance import Portfolio, Value_Portfolio, Trade, Trade_History


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

    @logger.catch
    async def trade(self, trade: Trade) -> Trade | None:
        response = await self.client.post("finance/execute", json=trade.model_dump())
        if response.status_code != 201:
            return

        return Trade.model_validate(response.json())

    @logger.catch
    async def history_trade(self, user_id) -> List[Trade_History] | None:
        response = await self.client.get(f"finance/history/{user_id}")
        if response.status_code != 200:
            return None
        trade_data = response.json()

        return [Trade_History(**trade) for trade in trade_data]
