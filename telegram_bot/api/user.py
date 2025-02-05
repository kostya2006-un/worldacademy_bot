from .base import BaseServer
from loguru import logger
from telegram_bot.schema.user import User, UserList


class UserAPI(BaseServer):

    @logger.catch
    async def get_user_by_id(self, user_id: str) -> User | None:
        response = await self.client.get(f"/users/{user_id}/")
        if response.status_code != 200:
            return

        return User.model_validate(response.json())

    @logger.catch
    async def get_users(self) -> UserList | None:
        response = await self.client.get(f"/users/")
        if response.status_code != 200:
            return None
        users_data = response.json()
        user_list = UserList.parse_obj({"user_id": [user["user_id"] for user in users_data]})
        return user_list

    @logger.catch
    async def create_user(self, user: User) -> User | None:
        response = await self.client.post("/users/", json=user.model_dump())
        if response.status_code != 201:
            return

        return User.model_validate(response.json())

    @logger.catch
    async def put_user(self, user: User) -> User | None:
        response = await self.client.put(
            f"/users/{user.id_user}/", json=user.model_dump()
        )

        if response.status_code != 200:
            return

        return User.model_validate(response.json())
