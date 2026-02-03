from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ModelCreate(BaseModel):
    name: str
    provider_id: int


class ModelUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    last_checked_at: Optional[datetime] = None


class ModelResponse(BaseModel):
    id: int
    name: str
    provider_id: int
    is_active: bool
    last_checked_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
