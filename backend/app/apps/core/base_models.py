from datetime import datetime

from settings import settings
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.sql import func

engine = create_async_engine(
    settings.DB_URL,
    echo=settings.DEBUG,
    pool_size=50,
    max_overflow=100,
    pool_pre_ping=True,
    pool_recycle=1800,
)


async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, sort_order=-10
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
