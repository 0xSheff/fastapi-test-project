import datetime

from apps.core.base_models import Base
from apps.users.constants import UserPermissionsEnum
from sqlalchemy import ARRAY, DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=True)
    permissions: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=lambda: [UserPermissionsEnum.CAN_SELF_DELETE],
        nullable=False,
        server_default=text("'{CAN_SELF_DELETE}'::text[]"),
    )
    use_token_since: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
