from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class AssistantCreate(BaseModel):
    name: Optional[str] = None


class AssistantUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    last_checked_at: Optional[datetime] = None


class AssistantResponse(BaseModel):
    id: int
    name: Optional[str]
    is_active: bool
    last_checked_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
