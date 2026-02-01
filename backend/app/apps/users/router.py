from apps.auth.dependencies import get_admin_user, get_current_user
from apps.core.dependencies import get_async_session
from apps.users.crud import user_manager
from apps.users.models import User
from apps.users.schemas import RegisteredUserSchema, RegisterUserSchema
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

users_router = APIRouter()


@users_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    new_user: RegisterUserSchema, session: AsyncSession = Depends(get_async_session)
) -> RegisteredUserSchema:
    created_user = await user_manager.create_user(new_user=new_user, session=session)
    return created_user


@users_router.get("/user-info")
async def get_my_info(user: User = Depends(get_current_user)) -> RegisteredUserSchema:
    return RegisteredUserSchema.model_validate(user)


@users_router.get("/{id}", dependencies=[Depends(get_admin_user)])
async def get_user(
    user_id: int = Path(..., description="The id of the user", ge=1, alias="id"),
    session: AsyncSession = Depends(get_async_session),
) -> RegisteredUserSchema:
    user: User | None = await user_manager.get(
        session=session, field_value=user_id, field=User.id
    )
    if not user:
        raise HTTPException(
            detail="User with given email not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return RegisteredUserSchema.model_validate(user)
