from fastapi import APIRouter, status

from apps.users.schemas import RegisterUserSchema, RegisteredUserSchema

users_router = APIRouter()


@users_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(new_user: RegisterUserSchema) -> RegisteredUserSchema:
    created_user = RegisteredUserSchema(id=8765776, **new_user.dict())
    return created_user
