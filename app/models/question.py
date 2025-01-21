from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.answer import Answer

if TYPE_CHECKING:
    from app.models.association import Association
    from app.models.category import Category


class Question(Base):
    title: Mapped[str] = mapped_column(String(256))
    additional: Mapped[str] = mapped_column(Text, nullable=True)
    text_question: Mapped[str] = mapped_column(Text)
    answers: Mapped[list['Answer']] = relationship(
        back_populates='question_answers'
    )
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped['Category'] = relationship(back_populates='question')
    blocks: Mapped[list['Association']] = relationship(
        back_populates='question'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
    interview_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=True
    )
    time_decision: Mapped[int] = mapped_column(
        Integer, default=10, nullable=True
    )

    def __repr__(self):
        return (
            f'{super().__repr__()}; {self.title=}; {self.additional=};'
            f'{self.interview_count=};'
            f'{self.time_decision=}; {self.category_id}'
        )
