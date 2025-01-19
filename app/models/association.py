from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.block import Block
    from app.models.question import Question


class Association(Base):
    question_id: Mapped[int] = mapped_column(ForeignKey('question.id'))
    block_id: Mapped[int] = mapped_column(ForeignKey('block.id'))

    question: Mapped['Question'] = relationship(back_populates='blocks')
    block: Mapped['Block'] = relationship(back_populates='questions')
