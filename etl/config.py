from pydantic import BaseSettings


class ETLSettings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "mg_saude_aps"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    class Config:
        env_file = ".env"


settings = ETLSettings()
