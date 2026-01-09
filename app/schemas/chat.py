from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChatCreate(BaseModel):
    user_id: int
    assistant_id: int


class ChatUpdate(BaseModel):
    assistant_id: Optional[int] = None


class ChatResponse(BaseModel):
    id: int
    user_id: int
    assistant_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
