from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category import CategoryService
from app.api.v1.endpoints.auth import get_current_admin_user
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("", response_model=list[CategoryResponse])
async def list_categories(
    only_top_level: bool = False,
    db: AsyncSession = Depends(get_db)
):
    return await CategoryService.get_all(db, only_top_level=only_top_level)

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: UUID, db: AsyncSession = Depends(get_db)):
    return await CategoryService.get(db, category_id)

@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    return await CategoryService.create(db, data)

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    return await CategoryService.update(db, category_id, data)

@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    await CategoryService.delete(db, category_id)
