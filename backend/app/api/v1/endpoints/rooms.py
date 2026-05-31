from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.room import (
    RoomCreate, RoomResponse, RoomJoin,
    RoomResourceAdd, RoomResourceResponse,
    RoomRatingCreate, RoomRatingResponse,
)
from app.services.room import RoomService
from app.api.v1.endpoints.auth import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.get("", response_model=list[RoomResponse])
async def list_rooms(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return await RoomService.list_member_rooms(db, user.id)

@router.post("", response_model=RoomResponse, status_code=201)
async def create_room(
    data: RoomCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return await RoomService.create(db, data, user.id)

@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: UUID, db: AsyncSession = Depends(get_db)):
    return await RoomService.get(db, room_id)

@router.put("/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: UUID,
    data: RoomCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return await RoomService.update(db, room_id, data, user.id)

@router.delete("/{room_id}", status_code=204)
async def delete_room(
    room_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    await RoomService.delete(db, room_id, user.id)

@router.post("/join")
async def join_room_by_code(
    data: RoomJoin,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return await RoomService.join_by_code(db, data, user.id)

@router.post("/{room_id}/join")
async def join_room(
    room_id: UUID,
    data: RoomJoin,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return await RoomService.join(db, room_id, data, user.id)

@router.get("/{room_id}/resources", response_model=list[RoomResourceResponse])
async def list_room_resources(room_id: UUID, db: AsyncSession = Depends(get_db)):
    return await RoomService.list_resources(db, room_id)

@router.post("/{room_id}/resources", response_model=RoomResourceResponse, status_code=201)
async def add_room_resource(
    room_id: UUID,
    data: RoomResourceAdd,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return await RoomService.add_resource(db, room_id, data.resource_id, user.id)

@router.get("/{room_id}/ratings/{resource_id}", response_model=list[RoomRatingResponse])
async def list_room_ratings(room_id: UUID, resource_id: UUID, db: AsyncSession = Depends(get_db)):
    return await RoomService.list_ratings(db, room_id, resource_id)

@router.post("/{room_id}/ratings/{resource_id}", response_model=RoomRatingResponse, status_code=201)
async def rate_room_resource(
    room_id: UUID,
    resource_id: UUID,
    data: RoomRatingCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return await RoomService.upsert_rating(db, room_id, resource_id, data, user.id)
