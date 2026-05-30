from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from uuid import UUID
from app.models.category import Category
from app.schemas.category import CategoryCreate

class CategoryService:
    @staticmethod
    async def list(db: AsyncSession) -> list[Category]:
        result = await db.execute(select(Category).order_by(Category.name))
        return result.scalars().all()

    @staticmethod
    async def get(db: AsyncSession, category_id: UUID) -> Category:
        result = await db.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return category

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> Category | None:
        result = await db.execute(select(Category).where(Category.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: CategoryCreate) -> Category:
        existing = await CategoryService.get_by_name(db, data.name)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")

        category = Category(name=data.name, parent_category_id=data.parent_category_id)
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def update(db: AsyncSession, category_id: UUID, data: CategoryCreate) -> Category:
        category = await CategoryService.get(db, category_id)

        dup = await db.execute(
            select(Category).where(Category.name == data.name, Category.id != category_id)
        )
        if dup.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category name already taken")

        category.name = data.name
        category.parent_category_id = data.parent_category_id
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def delete(db: AsyncSession, category_id: UUID) -> None:
        category = await CategoryService.get(db, category_id)
        await db.delete(category)
        await db.commit()
