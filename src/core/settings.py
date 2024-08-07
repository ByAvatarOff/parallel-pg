import os
from functools import cache
from src.transactions.schema.sql_schema import IsolationLevel, PostgresLock

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str = "Fast Postgres"
    description: str = "Fast Postgres"
    log_dir: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")


class DBSettings(BaseSettings):
    postgres_host: str
    postgres_db: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    isolation_level: IsolationLevel = IsolationLevel.READ_COMMITTED
    enabled_lock_table: PostgresLock = PostgresLock.NONE
    main_table_name: str = "warehouse"
    echo: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def _url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def async_url(self) -> str:
        return self._url()


class Settings:
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()


@cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
