from typing import TYPE_CHECKING

from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.questions import Question


class Answer(Base):
    content: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[str] = mapped_column(String(256))
    question: Mapped['Question'] = relationship(back_populates='answer')
