import socket

from fastapi import APIRouter
from settings import settings
from .schemas import BaseBackendInfoSchema, DatabaseInfoSchema

info_router = APIRouter()


@info_router.get("/backend")
async def get_backend_info() -> BaseBackendInfoSchema:
    return BaseBackendInfoSchema(backend=socket.gethostname())


@info_router.get("/database")
async def get_database_info() -> DatabaseInfoSchema:
    return DatabaseInfoSchema(database_url=settings.DB_URL)
