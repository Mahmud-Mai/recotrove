from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from app.core.database import get_db
from app.models.rating import Rating
from app.models.resource import Resource
from app.schemas.rating import RatingCreate, RatingResponse, AverageRating
from app.api.v1.endpoints.auth import get_current_active_user
from app.models.user import User

router = APIRouter(tags=["ratings"])

@router.get("/resources/{resource_id}/ratings", response_model=list[RatingResponse])
async def list_ratings(resource_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Rating).where(Rating.resource_id == resource_id).order_by(Rating.created_at.desc())
    )
    return result.scalars().all()

@router.post("/resources/{resource_id}/ratings", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
async def create_or_update_rating(
    resource_id: UUID,
    data: RatingCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    res_check = await db.execute(select(Resource).where(Resource.id == resource_id))
    if not res_check.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    result = await db.execute(
        select(Rating).where(Rating.resource_id == resource_id, Rating.user_id == user.id)
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
        user_id=user.id,
        rating=data.rating,
        review_text=data.review_text,
    )
    db.add(rating)
    await db.commit()
    await db.refresh(rating)
    return rating

@router.get("/resources/{resource_id}/average", response_model=AverageRating)
async def get_average_rating(resource_id: UUID, db: AsyncSession = Depends(get_db)):
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
