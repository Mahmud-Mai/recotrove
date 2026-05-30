from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class RatingCreate(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    review_text: Optional[str] = Field(None, max_length=1000)

class RatingResponse(BaseModel):
    id: UUID
    resource_id: UUID
    user_id: UUID
    rating: int
    review_text: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AverageRating(BaseModel):
    resource_id: UUID
    average: float = 0.0
    total: int = 0
