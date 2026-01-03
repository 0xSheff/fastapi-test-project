from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.crud import user_manager
from apps.users.schemas import RegisterUserSchema, RegisteredUserSchema
from apps.core.dependencies import get_async_session

users_router = APIRouter()


@users_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
        new_user: RegisterUserSchema,
        session: AsyncSession = Depends(get_async_session)
) -> RegisteredUserSchema:
    created_user = await user_manager.create_user(new_user=new_user, session=session)
    return created_user
