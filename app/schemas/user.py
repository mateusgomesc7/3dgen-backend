from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: Optional[EmailStr]
    name: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
