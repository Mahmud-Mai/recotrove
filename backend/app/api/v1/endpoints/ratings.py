from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.rating import RatingCreate, RatingResponse, AverageRating
from app.services.rating import RatingService
from app.api.v1.endpoints.auth import get_current_active_user
from app.models.user import User

router = APIRouter(tags=["ratings"])

@router.get("/resources/{resource_id}/ratings", response_model=list[RatingResponse])
async def list_ratings(resource_id: UUID, db: AsyncSession = Depends(get_db)):
    return await RatingService.list(db, resource_id)

@router.post("/resources/{resource_id}/ratings", response_model=RatingResponse, status_code=201)
async def create_or_update_rating(
    resource_id: UUID,
    data: RatingCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return await RatingService.upsert(db, resource_id, data, user.id)

@router.get("/resources/{resource_id}/average", response_model=AverageRating)
async def get_average_rating(resource_id: UUID, db: AsyncSession = Depends(get_db)):
    return await RatingService.get_average(db, resource_id)
