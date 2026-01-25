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


class JWTSettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_TIME_MINUTES: int = 5
    REFRESH_TOKEN_TIME_MINUTES: int = 60


class Settings(CoreSettings, DbSettings, JWTSettings):
    SENTRY_DSN: str
    BETTER_STACK_TOKEN: str
    BETTER_STACK_URL: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
