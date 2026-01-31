from datetime import datetime

from pydantic import BaseModel


class ChatCreate(BaseModel):
    user_id: int


class ChatResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
