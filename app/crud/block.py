from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models.block import Block
from app.schemas.block import BlockCreate, BlockUpdate


class CRUDBlock(CRUDBase[Block, BlockCreate, BlockUpdate]):

    async def get_by_title(
        self, session: AsyncSession, title: str
    ) -> Block | None:
        db_obj = await session.execute(
            select(self.model).where(self.model.title == title)
        )
        return db_obj.scalars().first()

    async def get_multy_by_title(
        self, session: AsyncSession, title: str
    ) -> list[Block] | None:
        all_blocks = await session.execute(
            select(self.model)
            .where(self.model.title == title)
            .options(joinedload(self.model.question_blocks))
        )
        return all_blocks.scalars().all()


block_crud = CRUDBlock(Block)
