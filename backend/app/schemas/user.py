from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

# Base schema (shared properties)
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

# Schema for creating a new user
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# Schema for API response (excludes sensitive data)
class UserResponse(UserBase):
    id: UUID
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Enables ORM mode

# Schema for login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for JWT token response
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[str] = None