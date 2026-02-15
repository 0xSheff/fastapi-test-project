import datetime as dt
from contextlib import asynccontextmanager

import redis.asyncio as redis
from settings import settings


class RedisService:
    @asynccontextmanager
    async def get_redis(self):
        _redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            username=settings.REDIS_USER if settings.REDIS_USER else None,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            db=settings.REDIS_DATABASE,
            decode_responses=True,
            socket_timeout=5,
            health_check_interval=30,
        )
        try:
            yield _redis
        finally:
            await _redis.close()

    async def set_cache(self, key: str, value: str | int, ttl: int = 60):
        async with self.get_redis() as _redis:
            await _redis.setex(key, dt.timedelta(seconds=ttl), value)

    async def get_cache(self, key: str):
        async with self.get_redis() as _redis:
            return await _redis.get(key)

    async def delete_cache(self, key: str):
        async with self.get_redis() as _redis:
            await _redis.delete(key)


redis_service = RedisService()
