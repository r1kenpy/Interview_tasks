from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.question import Question


class Block(Base):

    title: Mapped[str] = mapped_column(String(256))
    level: Mapped[int] = mapped_column(Integer, nullable=True)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('question.id')
    )
    question_blocks: Mapped[list['Question']] = relationship(
        back_populates='blocks'
    )

    def __repr__(self):
        return f'{super().__repr__()}; {self.title=}; {self.level=}; {self.question_id=}.'
