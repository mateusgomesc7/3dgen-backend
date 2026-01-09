from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class AssistantCreate(BaseModel):
    name: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None


class AssistantUpdate(BaseModel):
    name: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None


class AssistantResponse(BaseModel):
    id: int
    name: Optional[str]
    provider: Optional[str]
    model: Optional[str]

    class Config:
        from_attributes = True
