from typing import List
from .base import BaseServer
from loguru import logger
from telegram_bot.schema.asset import Asset


class AssetAPI(BaseServer):

    @logger.catch
    async def get_assets(self) -> List[Asset] | None:
        response = await self.client.get(f"/assets/")
        if response.status_code != 200:
            return None
        asset_data = response.json()

        return [Asset(**asset) for asset in asset_data]
