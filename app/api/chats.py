from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat import ChatCreate, ChatResponse
from app.schemas.common import PaginatedResponse
from app.schemas.message import MessageResponse
from app.services.chat_service import ChatService
from app.services.message_service import MessageService

router = APIRouter(prefix="/chats", tags=["Chats"])


def get_chat_service(db: Session = Depends(get_db)) -> ChatService:
    return ChatService(session=db)

def get_message_service(db: Session = Depends(get_db)) -> MessageService:
    return MessageService(session=db)


@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(
    chat_id: int,
    service: ChatService = Depends(get_chat_service)
):
    chat = service.get(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.get("/", response_model=PaginatedResponse[ChatResponse])
def list_chats(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[int] = Query(None),
    service: ChatService = Depends(get_chat_service),
):
    return service.paginated_list(
        page=page,
        page_size=page_size,
        user_id=user_id,
    )


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat(
    chat: ChatCreate,
    service: ChatService = Depends(get_chat_service)
):
    return service.create(chat)


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(
    chat_id: int,
    service: ChatService = Depends(get_chat_service)
):
    service.delete(chat_id)


@router.get("/{chat_id}/messages", response_model=list[MessageResponse])
def list_chat_messages(
    chat_id: int,
    service: MessageService = Depends(get_message_service)
):
    return service.list_by_chat(chat_id)
