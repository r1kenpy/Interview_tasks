from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (
    declarative_base,
    Mapped,
    mapped_column,
    declared_attr,
    sessionmaker,
)

from app.core.config import settings


class PreBase:
    """Базовая модель для всех таблиц."""

    @declared_attr
    def __tablename(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.db_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Получение сессии для работы с базой данных."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
