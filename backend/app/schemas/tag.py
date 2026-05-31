from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class TagCreate(BaseModel):
    name: str = Field(..., max_length=50)

class TagResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
