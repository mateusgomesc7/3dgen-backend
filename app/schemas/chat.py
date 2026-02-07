from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChatCreate(BaseModel):
    user_id: int
    user_prompt: Optional[str] = None


class ChatResponse(BaseModel):
    id: int
    user_id: int
    name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatRename(BaseModel):
    name: str
