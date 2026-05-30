from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class ResourceCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    thumbnail_url: Optional[str] = None
    external_link: Optional[str] = None
    category_id: UUID

class ResourceUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    thumbnail_url: Optional[str] = None
    external_link: Optional[str] = None
    category_id: Optional[UUID] = None

class ResourceResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    external_link: Optional[str] = None
    category_id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ResourceListResponse(ResourceResponse):
    average_rating: float = 0.0
    total_ratings: int = 0
