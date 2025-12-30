import socket

from fastapi import APIRouter
from settings import settings

info_router = APIRouter()


@info_router.get("/backend")
async def get_backend_info():
    return {"backend": socket.gethostname()}


@info_router.get("/database")
async def get_database_info():
    return {"database_url": settings.DB_URL}
