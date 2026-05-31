from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from uuid import UUID
import secrets
from app.models.room import Room, RoomMember, RoomResource, RoomRating
from app.models.resource import Resource
from app.schemas.room import RoomCreate, RoomJoin, RoomRatingCreate

class RoomService:
    @staticmethod
    async def list_member_rooms(db: AsyncSession, user_id: UUID) -> list[Room]:
        result = await db.execute(
            select(
                Room,
                func.count(RoomMember.user_id).label("member_count")
            )
            .join(RoomMember, RoomMember.room_id == Room.id, isouter=True)
            .where((Room.owner_id == user_id) | (RoomMember.user_id == user_id))
            .group_by(Room.id)
            .order_by(Room.created_at.desc())
        )
        
        rooms = []
        for row in result.all():
            room = row[0]
            room.member_count = row.member_count
            rooms.append(room)
        return rooms

    @staticmethod
    async def get(db: AsyncSession, room_id: UUID) -> Room:
        result = await db.execute(
            select(
                Room,
                func.count(RoomMember.user_id).label("member_count")
            )
            .join(RoomMember, RoomMember.room_id == Room.id, isouter=True)
            .where(Room.id == room_id)
            .group_by(Room.id)
        )
        row = result.one_or_none()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        
        room = row[0]
        room.member_count = row.member_count
        return room

    @staticmethod
    async def _get_owned(db: AsyncSession, room_id: UUID, user_id: UUID) -> Room:
        room = await RoomService.get(db, room_id)
        if room.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not the owner")
        return room

    @staticmethod
    async def create(db: AsyncSession, data: RoomCreate, user_id: UUID) -> Room:
        invite_code = secrets.token_hex(4)

        room = Room(
            name=data.name,
            description=data.description,
            owner_id=user_id,
            invite_code=invite_code,
        )
        db.add(room)
        await db.flush()

        member = RoomMember(room_id=room.id, user_id=user_id)
        db.add(member)

        await db.commit()
        await db.refresh(room)
        return room

    @staticmethod
    async def update(db: AsyncSession, room_id: UUID, data: RoomCreate, user_id: UUID) -> Room:
        room = await RoomService._get_owned(db, room_id, user_id)

        room.name = data.name
        room.description = data.description
        await db.commit()
        await db.refresh(room)
        return room

    @staticmethod
    async def delete(db: AsyncSession, room_id: UUID, user_id: UUID) -> None:
        room = await RoomService._get_owned(db, room_id, user_id)
        await db.delete(room)
        await db.commit()

    @staticmethod
    async def join(db: AsyncSession, room_id: UUID, data: RoomJoin, user_id: UUID) -> dict:
        room = await RoomService.get(db, room_id)

        if room.invite_code != data.invite_code:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid invite code")

        member_check = await db.execute(
            select(RoomMember).where(RoomMember.room_id == room_id, RoomMember.user_id == user_id)
        )
        if member_check.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already a member")

        member = RoomMember(room_id=room_id, user_id=user_id)
        db.add(member)
        await db.commit()
        return {"detail": "Joined room", "room_id": str(room_id)}

    @staticmethod
    async def join_by_code(db: AsyncSession, data: RoomJoin, user_id: UUID) -> dict:
        result = await db.execute(select(Room).where(Room.invite_code == data.invite_code))
        room = result.scalar_one_or_none()
        
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid invite code")

        member_check = await db.execute(
            select(RoomMember).where(RoomMember.room_id == room.id, RoomMember.user_id == user_id)
        )
        if member_check.scalar_one_or_none():
            return {"detail": "Already a member", "room_id": str(room.id)}

        member = RoomMember(room_id=room.id, user_id=user_id)
        db.add(member)
        await db.commit()
        return {"detail": "Joined room", "room_id": str(room.id)}

    @staticmethod
    async def list_resources(db: AsyncSession, room_id: UUID) -> list[dict]:
        # We want to return RoomResource joined with Resource, 
        # plus room-specific average ratings
        query = (
            select(
                RoomResource,
                Resource,
                func.coalesce(func.avg(RoomRating.rating), 0).label("room_avg"),
                func.count(RoomRating.id).label("room_count")
            )
            .join(Resource, Resource.id == RoomResource.resource_id)
            .outerjoin(
                RoomRating, 
                (RoomRating.room_id == RoomResource.room_id) & 
                (RoomRating.resource_id == RoomResource.resource_id)
            )
            .where(RoomResource.room_id == room_id)
            .group_by(RoomResource.room_id, RoomResource.resource_id, Resource.id)
            .options(selectinload(Resource.tags))
            .order_by(RoomResource.added_at.desc())
        )
        
        result = await db.execute(query)
        rows = result.all()
        
        from app.schemas.resource import ResourceListResponse
        from app.schemas.tag import TagResponse

        output = []
        for rr, res, avg, count in rows:
            res_dto = ResourceListResponse(
                id=res.id,
                title=res.title,
                description=res.description,
                thumbnail_url=res.thumbnail_url,
                external_link=res.external_link,
                category_id=res.category_id,
                created_by=res.created_by,
                created_at=res.created_at,
                updated_at=res.updated_at,
                tags=[TagResponse.model_validate(t) for t in res.tags],
                average_rating=round(float(avg), 1),
                total_ratings=count,
            )
            output.append({
                "room_id": rr.room_id,
                "resource_id": rr.resource_id,
                "added_by": rr.added_by,
                "added_at": rr.added_at,
                "resource": res_dto
            })
        return output

    @staticmethod
    async def add_resource(db: AsyncSession, room_id: UUID, resource_id: UUID, user_id: UUID) -> dict:
        room_check = await db.execute(select(Room).where(Room.id == room_id))
        if not room_check.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

        res_check = await db.execute(
            select(Resource).where(Resource.id == resource_id).options(selectinload(Resource.tags))
        )
        res = res_check.scalar_one_or_none()
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

        dup = await db.execute(
            select(RoomResource).where(RoomResource.room_id == room_id, RoomResource.resource_id == resource_id)
        )
        if dup.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource already in room")

        rr = RoomResource(room_id=room_id, resource_id=resource_id, added_by=user_id)
        db.add(rr)
        await db.commit()
        await db.refresh(rr)
        
        from app.schemas.resource import ResourceListResponse
        from app.schemas.tag import TagResponse
        
        res_dto = ResourceListResponse(
            id=res.id,
            title=res.title,
            description=res.description,
            thumbnail_url=res.thumbnail_url,
            external_link=res.external_link,
            category_id=res.category_id,
            created_by=res.created_by,
            created_at=res.created_at,
            updated_at=res.updated_at,
            tags=[TagResponse.model_validate(t) for t in res.tags],
            average_rating=0.0,
            total_ratings=0,
        )

        return {
            "room_id": rr.room_id,
            "resource_id": rr.resource_id,
            "added_by": rr.added_by,
            "added_at": rr.added_at,
            "resource": res_dto
        }

    @staticmethod
    async def list_ratings(db: AsyncSession, room_id: UUID, resource_id: UUID) -> list[RoomRating]:
        result = await db.execute(
            select(RoomRating).where(
                RoomRating.room_id == room_id, RoomRating.resource_id == resource_id
            ).order_by(RoomRating.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def upsert_rating(
        db: AsyncSession, room_id: UUID, resource_id: UUID, data: RoomRatingCreate, user_id: UUID
    ) -> RoomRating:
        room_check = await db.execute(select(Room).where(Room.id == room_id))
        if not room_check.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

        existing = await db.execute(
            select(RoomRating).where(
                RoomRating.room_id == room_id,
                RoomRating.resource_id == resource_id,
                RoomRating.user_id == user_id,
            )
        )
        existing_rating = existing.scalar_one_or_none()
        if existing_rating:
            existing_rating.rating = data.rating
            existing_rating.review_text = data.review_text
            await db.commit()
            await db.refresh(existing_rating)
            return existing_rating

        rr = RoomRating(
            room_id=room_id,
            resource_id=resource_id,
            user_id=user_id,
            rating=data.rating,
            review_text=data.review_text,
        )
        db.add(rr)
        await db.commit()
        await db.refresh(rr)
        return rr
