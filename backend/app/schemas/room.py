from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.schemas.resource import ResourceListResponse

class RoomCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None

class RoomResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    owner_id: UUID
    invite_code: str
    is_private: bool
    created_at: datetime
    member_count: int = 0

    class Config:
        from_attributes = True

class RoomJoin(BaseModel):
    invite_code: str

class RoomResourceAdd(BaseModel):
    resource_id: UUID

class RoomResourceResponse(BaseModel):
    room_id: UUID
    resource_id: UUID
    added_by: UUID
    added_at: datetime
    resource: ResourceListResponse

    class Config:
        from_attributes = True

class RoomRatingCreate(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    review_text: Optional[str] = Field(None, max_length=1000)

class RoomRatingResponse(BaseModel):
    id: UUID
    room_id: UUID
    resource_id: UUID
    user_id: UUID
    rating: int
    review_text: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
