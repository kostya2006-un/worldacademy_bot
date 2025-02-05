from httpx import AsyncClient


class BaseServer:

    def __init__(self, server_host: str):
        self.client = AsyncClient(
            base_url=f"{server_host}",
        )
