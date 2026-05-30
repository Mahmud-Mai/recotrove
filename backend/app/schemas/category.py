from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    parent_category_id: Optional[UUID] = None

class CategoryResponse(BaseModel):
    id: UUID
    name: str
    is_admin_created: bool
    parent_category_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True
