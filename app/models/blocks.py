from typing import TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.questions import Question


class Block(Base):

    title: Mapped[str] = mapped_column(String(256))
    level: Mapped[int] = mapped_column(Integer)
    question: Mapped['Question'] = relationship(back_populates='block')
