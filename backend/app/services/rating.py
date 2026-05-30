from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
from uuid import UUID
from app.models.rating import Rating
from app.models.resource import Resource
from app.schemas.rating import RatingCreate, AverageRating

class RatingService:
    @staticmethod
    async def list(db: AsyncSession, resource_id: UUID) -> list[Rating]:
        result = await db.execute(
            select(Rating).where(Rating.resource_id == resource_id).order_by(Rating.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def upsert(db: AsyncSession, resource_id: UUID, data: RatingCreate, user_id: UUID) -> Rating:
        res_check = await db.execute(select(Resource).where(Resource.id == resource_id))
        if not res_check.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

        result = await db.execute(
            select(Rating).where(Rating.resource_id == resource_id, Rating.user_id == user_id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.rating = data.rating
            existing.review_text = data.review_text
            await db.commit()
            await db.refresh(existing)
            return existing

        rating = Rating(
            resource_id=resource_id,
            user_id=user_id,
            rating=data.rating,
            review_text=data.review_text,
        )
        db.add(rating)
        await db.commit()
        await db.refresh(rating)
        return rating

    @staticmethod
    async def get_average(db: AsyncSession, resource_id: UUID) -> AverageRating:
        result = await db.execute(
            select(
                func.coalesce(func.avg(Rating.rating), 0).label("average"),
                func.count(Rating.id).label("total"),
            ).where(Rating.resource_id == resource_id)
        )
        row = result.one()
        return AverageRating(
            resource_id=resource_id,
            average=round(float(row.average), 1),
            total=row.total,
        )
