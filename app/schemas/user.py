from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    name: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
