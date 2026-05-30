from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.resource import ResourceCreate, ResourceUpdate, ResourceListResponse
from app.services.resource import ResourceService
from app.api.v1.endpoints.auth import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/resources", tags=["resources"])

@router.get("", response_model=list[ResourceListResponse])
async def list_resources(
    category_id: UUID = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await ResourceService.list(db, category_id)

@router.get("/{resource_id}", response_model=ResourceListResponse)
async def get_resource(resource_id: UUID, db: AsyncSession = Depends(get_db)):
    return await ResourceService.get(db, resource_id)

@router.post("", response_model=ResourceListResponse, status_code=201)
async def create_resource(
    data: ResourceCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return await ResourceService.create(db, data, user.id)

@router.put("/{resource_id}", response_model=ResourceListResponse)
async def update_resource(
    resource_id: UUID,
    data: ResourceUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return await ResourceService.update(db, resource_id, data, user.id)

@router.delete("/{resource_id}", status_code=204)
async def delete_resource(
    resource_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    await ResourceService.delete(db, resource_id, user.id)
