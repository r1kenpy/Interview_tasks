from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.question import Question


class Answer(Base):

    content: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[str] = mapped_column(String(256))
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('question.id')
    )
    question_answers: Mapped['Question'] = relationship(
        back_populates='answers'
    )

    def __repr__(self):
        return f'{super().__repr__()}; {self.content=}; {self.difficulty=}; {self.question_id=}.'
