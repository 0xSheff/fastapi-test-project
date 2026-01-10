from functools import lru_cache

from pydantic_settings import BaseSettings


class CoreSettings(BaseSettings):
    APP_NAME: str = "Test Project Shop"
    DEBUG: bool = False


class DbSettings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Settings(CoreSettings, DbSettings):
    SENTRY_DSN: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
