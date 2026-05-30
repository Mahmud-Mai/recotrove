from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
import secrets
from app.core.database import get_db
from app.models.room import Room, RoomMember, RoomResource, RoomRating
from app.models.resource import Resource
from app.schemas.room import (
    RoomCreate, RoomResponse, RoomJoin,
    RoomResourceAdd, RoomResourceResponse,
    RoomRatingCreate, RoomRatingResponse,
)
from app.api.v1.endpoints.auth import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.get("", response_model=list[RoomResponse])
async def list_rooms(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    result = await db.execute(
        select(Room).join(RoomMember, RoomMember.room_id == Room.id, isouter=True)
        .where((Room.owner_id == user.id) | (RoomMember.user_id == user.id))
        .distinct().order_by(Room.created_at.desc())
    )
    return result.scalars().all()

@router.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    data: RoomCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    invite_code = secrets.token_hex(4)

    room = Room(
        name=data.name,
        description=data.description,
        owner_id=user.id,
        invite_code=invite_code,
    )
    db.add(room)
    await db.flush()

    member = RoomMember(room_id=room.id, user_id=user.id)
    db.add(member)

    await db.commit()
    await db.refresh(room)
    return room

@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room

@router.put("/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: UUID,
    data: RoomCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if room.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not the owner")

    room.name = data.name
    room.description = data.description
    await db.commit()
    await db.refresh(room)
    return room

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if room.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not the owner")
    await db.delete(room)
    await db.commit()

@router.post("/{room_id}/join")
async def join_room(
    room_id: UUID,
    data: RoomJoin,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if room.invite_code != data.invite_code:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid invite code")

    member_check = await db.execute(
        select(RoomMember).where(RoomMember.room_id == room_id, RoomMember.user_id == user.id)
    )
    if member_check.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already a member")

    member = RoomMember(room_id=room_id, user_id=user.id)
    db.add(member)
    await db.commit()
    return {"detail": "Joined room", "room_id": str(room_id)}

@router.get("/{room_id}/resources", response_model=list[RoomResourceResponse])
async def list_room_resources(room_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RoomResource).where(RoomResource.room_id == room_id).order_by(RoomResource.added_at.desc())
    )
    return result.scalars().all()

@router.post("/{room_id}/resources", response_model=RoomResourceResponse, status_code=status.HTTP_201_CREATED)
async def add_room_resource(
    room_id: UUID,
    data: RoomResourceAdd,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    room_check = await db.execute(select(Room).where(Room.id == room_id))
    if not room_check.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    res_check = await db.execute(select(Resource).where(Resource.id == data.resource_id))
    if not res_check.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    dup = await db.execute(
        select(RoomResource).where(RoomResource.room_id == room_id, RoomResource.resource_id == data.resource_id)
    )
    if dup.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource already in room")

    rr = RoomResource(room_id=room_id, resource_id=data.resource_id, added_by=user.id)
    db.add(rr)
    await db.commit()
    await db.refresh(rr)
    return rr

@router.get("/{room_id}/ratings/{resource_id}", response_model=list[RoomRatingResponse])
async def list_room_ratings(room_id: UUID, resource_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RoomRating).where(
            RoomRating.room_id == room_id, RoomRating.resource_id == resource_id
        ).order_by(RoomRating.created_at.desc())
    )
    return result.scalars().all()

@router.post("/{room_id}/ratings/{resource_id}", response_model=RoomRatingResponse, status_code=status.HTTP_201_CREATED)
async def rate_room_resource(
    room_id: UUID,
    resource_id: UUID,
    data: RoomRatingCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    room_check = await db.execute(select(Room).where(Room.id == room_id))
    if not room_check.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    existing = await db.execute(
        select(RoomRating).where(
            RoomRating.room_id == room_id,
            RoomRating.resource_id == resource_id,
            RoomRating.user_id == user.id,
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
        user_id=user.id,
        rating=data.rating,
        review_text=data.review_text,
    )
    db.add(rr)
    await db.commit()
    await db.refresh(rr)
    return rr
