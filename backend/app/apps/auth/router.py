from apps.auth.auth_handler import auth_handler
from apps.auth.dependencies import get_current_user
from apps.auth.schemas import ForceLogoutSchema, LoginResponseSchema
from apps.core.dependencies import get_async_session
from apps.users.crud import user_manager
from apps.users.models import User
from fastapi import APIRouter, Depends, Header, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

router_auth = APIRouter()


@router_auth.post("/login", response_model=LoginResponseSchema)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> LoginResponseSchema:
    token_pair = await auth_handler.get_login_token_pairs(session, data)
    return token_pair


@router_auth.post("/refresh", response_model=LoginResponseSchema)
async def refresh_user_token(
    refresh_token: str = Header(..., alias="refresh-token"),
    session: AsyncSession = Depends(get_async_session),
) -> LoginResponseSchema:
    token_pair = await auth_handler.get_refresh_token_pair(refresh_token, session)
    return token_pair


@router_auth.post("/force-logout", status_code=status.HTTP_204_NO_CONTENT)
async def force_logout(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await user_manager.patch(
        user.id, data_to_patch=ForceLogoutSchema(), session=session, exclude_unset=False
    )
