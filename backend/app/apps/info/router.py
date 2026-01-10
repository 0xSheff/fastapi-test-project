import socket

from fastapi import APIRouter
from settings import settings

from .schemas import BaseBackendInfoSchema, DatabaseInfoSchema

info_router = APIRouter()


@info_router.get("/backend")
async def get_backend_info() -> BaseBackendInfoSchema:
    # betterstack_logger.info(
    #     "some info29999",
    #     extra={
    #         "user_id": 234,
    #         "debug_info": {"function": "get_backend_info", "status": "OK"},
    #     },
    # )
    # betterstack_logger.error(
    #     "some info2777",
    #     extra={
    #         "user_id": 555,
    #         "debug_info": {"function": "get_backend_info", "status": "OK"},
    #     },
    # )
    return BaseBackendInfoSchema(backend=socket.gethostname())


@info_router.get("/database")
async def get_database_info() -> DatabaseInfoSchema:
    return DatabaseInfoSchema(database_url=settings.DB_URL)
