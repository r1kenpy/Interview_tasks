from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryCRUD(CRUDBase[Category, CategoryCreate, CategoryUpdate]):

    def __init__(self, model: Category) -> None:
        self.model = model

    async def get_category_by_title(
        self, session: AsyncSession, title
    ) -> Category | None:
        category = await session.execute(
            select(self.model).where(self.model.title == title)
        )
        return category.scalars().first()


category_crud = CategoryCRUD(Category)
