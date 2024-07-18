from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    root_path: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
