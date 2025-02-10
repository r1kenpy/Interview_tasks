from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.answer import Answer


class Difficulty(Base):
    __tablename__ = 'difficulties'

    title: Mapped[str] = mapped_column(
        String(100), default='Сложность отсутствует'
    )
    answers: Mapped[list['Answer']] = relationship(back_populates='difficulty')
