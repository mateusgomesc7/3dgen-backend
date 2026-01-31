from datetime import datetime
from pydantic import BaseModel
from typing import Literal, Optional


class MessageCreate(BaseModel):
    chat_id: int
    assistant_id: Optional[int] = None
    role: Literal["user", "assistant", "system"]
    content: str

class MasssageUpdate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    chat_id: int
    assistant_id: Optional[int] = None
    role: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
