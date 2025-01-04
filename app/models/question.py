from typing import Union, List
from datetime import datetime

from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.answer import Answer
from app.models.block import Block


class Question(Base):
    title: Mapped[str] = mapped_column(String(256))
    additional: Mapped[str] = mapped_column(Text, nullable=True)
    answers: Mapped[list['Answer']] = relationship(
        back_populates='question_answers'
    )
    blocks: Mapped[list['Block']] = relationship(
        back_populates='question_blocks'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
    interview_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=True
    )
    time_decision: Mapped[int] = mapped_column(Integer, default=10)

    def __repr__(self):
        return (
            f'{super().__repr__()}; {self.title=}; {self.additional=};'
            f'{self.interview_count=};'
            f'{self.time_decision=}'
        )
