from pydantic import Field
from typing import Annotated, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    telegram_token: str
    main_channel_id: str
    redis_uri: Annotated[Optional[str], Field(default=None)]
    server_host: str
    server_token: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
