import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "MG Saúde APS"
    ENV: str = "dev"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "mg_saude_aps"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
