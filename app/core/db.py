from dataclasses import dataclass

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (
    declarative_base,
    Mapped,
    mapped_column,
    declared_attr,
    sessionmaker,
    DeclarativeBase,
)

from app.core.config import settings


@dataclass
class Base(DeclarativeBase):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


engine = create_async_engine(settings.database_url, echo=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Получение сессии для работы с базой данных."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
