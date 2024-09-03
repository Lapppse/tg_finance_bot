import os
from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class BotSettings(BaseSettings):
    token: SecretStr
    current_db_path: str
    model_config = SettingsConfigDict(env_file=DOTENV)


config = BotSettings(_env_file=".env", _env_file_encoding="utf-8")  # pyright: ignore
