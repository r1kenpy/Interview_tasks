from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.question import Question


class Category(Base):
    title: Mapped[str] = mapped_column(String(256), nullable=True, unique=True)
    question: Mapped['Question'] = relationship(back_populates='category')
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
