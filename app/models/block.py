from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.association import Association


class Block(Base):

    title: Mapped[str] = mapped_column(String(256))
    level: Mapped[int] = mapped_column(Integer, nullable=True)
    questions: Mapped[list['Association']] = relationship(
        back_populates='block'
    )

    def __repr__(self):
        return f'{super().__repr__()}; {self.title=}; {self.level=}.'
