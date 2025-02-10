from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.association import Association


class Block(Base):

    title: Mapped[str] = mapped_column(String(256), unique=True)
    level: Mapped[int] = mapped_column(Integer, nullable=True, unique=True)
    questions: Mapped[list['Association']] = relationship(
        back_populates='block'
    )
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self):
        return f'{super().__repr__()}; {self.title=}; {self.level=}.'
