from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from uuid import UUID
from app.models.resource import Resource
from app.models.rating import Rating
from app.models.category import Category
from app.models.tag import Tag
from app.schemas.resource import ResourceCreate, ResourceUpdate, ResourceListResponse
from app.schemas.tag import TagResponse

class ResourceService:
    @staticmethod
    async def list(db: AsyncSession, category_id: UUID | None = None) -> list[ResourceListResponse]:
        query = select(
            Resource,
            func.coalesce(func.avg(Rating.rating), 0).label("average_rating"),
            func.count(Rating.id).label("total_ratings"),
        ).outerjoin(Rating, Rating.resource_id == Resource.id).options(selectinload(Resource.tags))

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
                tags=[TagResponse.model_validate(t) for t in row[0].tags],
                average_rating=round(float(row.average_rating), 1),
                total_ratings=row.total_ratings,
            )
            for row in rows
        ]

    @staticmethod
    async def get(db: AsyncSession, resource_id: UUID) -> ResourceListResponse:
        result = await db.execute(
            select(
                Resource,
                func.coalesce(func.avg(Rating.rating), 0).label("average_rating"),
                func.count(Rating.id).label("total_ratings"),
            ).outerjoin(Rating, Rating.resource_id == Resource.id)
            .where(Resource.id == resource_id)
            .group_by(Resource.id)
            .options(selectinload(Resource.tags))
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
            tags=[TagResponse.model_validate(t) for t in row[0].tags],
            average_rating=round(float(row.average_rating), 1),
            total_ratings=row.total_ratings,
        )

    @staticmethod
    async def _get_raw(db: AsyncSession, resource_id: UUID) -> Resource:
        result = await db.execute(
            select(Resource).where(Resource.id == resource_id).options(selectinload(Resource.tags))
        )
        resource = result.scalar_one_or_none()
        if not resource:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
        return resource

    @staticmethod
    async def _get_or_create_tags(db: AsyncSession, tag_names: list[str]) -> list[Tag]:
        tags = []
        for name in tag_names:
            name = name.lower().strip()
            result = await db.execute(select(Tag).where(Tag.name == name))
            tag = result.scalar_one_or_none()
            if not tag:
                tag = Tag(name=name)
                db.add(tag)
            tags.append(tag)
        return tags

    @staticmethod
    async def create(db: AsyncSession, data: ResourceCreate, user_id: UUID) -> ResourceListResponse:
        cat_check = await db.execute(select(Category).where(Category.id == data.category_id))
        if not cat_check.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")

        # Extract tags and remove from model dump
        tag_names = data.tags
        resource_data = data.model_dump(exclude={"tags"})
        
        resource = Resource(**resource_data, created_by=user_id)
        resource.tags = await ResourceService._get_or_create_tags(db, tag_names)
        
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
            tags=[TagResponse.model_validate(t) for t in resource.tags],
            average_rating=0.0,
            total_ratings=0,
        )

    @staticmethod
    async def update(db: AsyncSession, resource_id: UUID, data: ResourceUpdate, user_id: UUID) -> ResourceListResponse:
        resource = await ResourceService._get_raw(db, resource_id)

        if resource.created_by != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not the owner")

        update_data = data.model_dump(exclude_unset=True)
        
        if "tags" in update_data:
            tag_names = update_data.pop("tags")
            resource.tags = await ResourceService._get_or_create_tags(db, tag_names)

        for field, value in update_data.items():
            setattr(resource, field, value)

        await db.commit()
        await db.refresh(resource)

        average_rating, total_ratings = await ResourceService._get_avg_data(db, resource.id)

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
            tags=[TagResponse.model_validate(t) for t in resource.tags],
            average_rating=average_rating,
            total_ratings=total_ratings,
        )

    @staticmethod
    async def delete(db: AsyncSession, resource_id: UUID, user_id: UUID) -> None:
        resource = await ResourceService._get_raw(db, resource_id)

        if resource.created_by != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not the owner")

        await db.delete(resource)
        await db.commit()
