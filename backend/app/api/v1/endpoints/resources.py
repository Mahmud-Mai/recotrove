from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from app.core.database import get_db
from app.models.resource import Resource
from app.models.rating import Rating
from app.models.category import Category
from app.schemas.resource import ResourceCreate, ResourceUpdate, ResourceListResponse
from app.api.v1.endpoints.auth import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/resources", tags=["resources"])

@router.get("", response_model=list[ResourceListResponse])
async def list_resources(
    category_id: UUID = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(
        Resource,
        func.coalesce(func.avg(Rating.rating), 0).label("average_rating"),
        func.count(Rating.id).label("total_ratings"),
    ).outerjoin(Rating, Rating.resource_id == Resource.id)

    if category_id:
        query = query.where(Resource.category_id == category_id)

    query = query.group_by(Resource.id).order_by(Resource.created_at.desc())
    result = await db.execute(query)
    rows = result.all()

    return [
        ResourceListResponse(
            id=row[0].id,
            title=row[0].title,
            description=row[0].description,
            thumbnail_url=row[0].thumbnail_url,
            external_link=row[0].external_link,
            category_id=row[0].category_id,
            created_by=row[0].created_by,
            created_at=row[0].created_at,
            updated_at=row[0].updated_at,
            average_rating=round(float(row.average_rating), 1),
            total_ratings=row.total_ratings,
        )
        for row in rows
    ]

@router.get("/{resource_id}", response_model=ResourceListResponse)
async def get_resource(resource_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Resource,
            func.coalesce(func.avg(Rating.rating), 0).label("average_rating"),
            func.count(Rating.id).label("total_ratings"),
        ).outerjoin(Rating, Rating.resource_id == Resource.id)
        .where(Resource.id == resource_id)
        .group_by(Resource.id)
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    return ResourceListResponse(
        id=row[0].id,
        title=row[0].title,
        description=row[0].description,
        thumbnail_url=row[0].thumbnail_url,
        external_link=row[0].external_link,
        category_id=row[0].category_id,
        created_by=row[0].created_by,
        created_at=row[0].created_at,
        updated_at=row[0].updated_at,
        average_rating=round(float(row.average_rating), 1),
        total_ratings=row.total_ratings,
    )

@router.post("", response_model=ResourceListResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    data: ResourceCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    cat_check = await db.execute(select(Category).where(Category.id == data.category_id))
    if not cat_check.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")

    resource = Resource(
        title=data.title,
        description=data.description,
        thumbnail_url=data.thumbnail_url,
        external_link=data.external_link,
        category_id=data.category_id,
        created_by=user.id,
    )
    db.add(resource)
    await db.commit()
    await db.refresh(resource)

    return ResourceListResponse(
        id=resource.id,
        title=resource.title,
        description=resource.description,
        thumbnail_url=resource.thumbnail_url,
        external_link=resource.external_link,
        category_id=resource.category_id,
        created_by=resource.created_by,
        created_at=resource.created_at,
        updated_at=resource.updated_at,
        average_rating=0.0,
        total_ratings=0,
    )

@router.put("/{resource_id}", response_model=ResourceListResponse)
async def update_resource(
    resource_id: UUID,
    data: ResourceUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    resource = result.scalar_one_or_none()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    if resource.created_by != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not the owner")

    if data.title is not None:
        resource.title = data.title
    if data.description is not None:
        resource.description = data.description
    if data.thumbnail_url is not None:
        resource.thumbnail_url = data.thumbnail_url
    if data.external_link is not None:
        resource.external_link = data.external_link
    if data.category_id is not None:
        resource.category_id = data.category_id

    await db.commit()
    await db.refresh(resource)

    avg_result = await db.execute(
        select(
            func.coalesce(func.avg(Rating.rating), 0).label("average_rating"),
            func.count(Rating.id).label("total_ratings"),
        ).where(Rating.resource_id == resource.id)
    )
    avg = avg_result.one()

    return ResourceListResponse(
        id=resource.id,
        title=resource.title,
        description=resource.description,
        thumbnail_url=resource.thumbnail_url,
        external_link=resource.external_link,
        category_id=resource.category_id,
        created_by=resource.created_by,
        created_at=resource.created_at,
        updated_at=resource.updated_at,
        average_rating=round(float(avg.average_rating), 1),
        total_ratings=avg.total_ratings,
    )

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    resource_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    resource = result.scalar_one_or_none()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    if resource.created_by != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not the owner")
    await db.delete(resource)
    await db.commit()
