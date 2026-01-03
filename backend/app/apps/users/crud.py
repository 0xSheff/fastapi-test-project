from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.password_handler import PasswordEncrypt
from apps.core.base_crud import BaseCRUDManager
from apps.users.models import User
from apps.users.schemas import RegisterUserSchema


class UserCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model= User

    async def create_user(self, new_user: RegisterUserSchema, session: AsyncSession) -> User:
        existing_user = await self.get(session=session, field=self.model.email, field_value=new_user.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        hashed_password = await PasswordEncrypt.get_password_hash(new_user.password)
        user = await self.create(
            session=session,
            email=new_user.email,
            hashed_password=hashed_password,
            name=new_user.name,
        )
        return user


user_manager = UserCRUDManager()