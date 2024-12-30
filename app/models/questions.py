from datetime import datetime

from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.answers import Answer
from app.models.blocks import Block


class Question(Base):
    title: Mapped[str] = mapped_column(String(256))
    additional: Mapped[str] = mapped_column(Text, nullable=True)

    answer_id: Mapped[int] = mapped_column(ForeignKey('answer.id'))
    answer: Mapped[list['Answer']] = relationship(back_populates='question')

    block_id: Mapped[int] = mapped_column(ForeignKey('block.id'))
    block: Mapped[list['Block']] = relationship(back_populates='question')
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
    interview_count: Mapped[int] = mapped_column(Integer, default=0)
    time_decision: Mapped[int] = mapped_column(Integer)
