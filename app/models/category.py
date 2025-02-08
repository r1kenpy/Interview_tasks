from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.question import Question


class Category(Base):
    title: Mapped[str] = mapped_column(String(256), nullable=True)
    question: Mapped['Question'] = relationship(back_populates='category')
