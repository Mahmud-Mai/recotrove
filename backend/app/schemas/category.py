from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=100)
    parent_category_id: Optional[UUID] = None

class CategoryResponse(BaseModel):
    id: UUID
    name: str
    is_admin_created: bool
    parent_category_id: Optional[UUID] = None
    created_at: datetime
    children: List["CategoryResponse"] = []

    class Config:
        from_attributes = True

CategoryResponse.model_rebuild()

