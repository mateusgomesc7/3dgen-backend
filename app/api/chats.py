from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat import ChatCreate, ChatRename, ChatResponse
from app.schemas.common import PaginatedResponse
from app.schemas.message import MessageResponse
from app.services.chat_service import ChatService
from app.services.message_service import MessageService

router = APIRouter(prefix='/chats', tags=['Chats'])


def get_chat_service(db: Annotated[Session, Depends(get_db)]) -> ChatService:
    return ChatService(session=db)


def get_message_service(db: Annotated[Session, Depends(get_db)]) -> MessageService:
    return MessageService(session=db)


ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]

MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]


@router.get('/{chat_id}', response_model=ChatResponse)
def get_chat(chat_id: int, service: ChatServiceDep):
    chat = service.get(chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Chat not found'
        )
    return chat


@router.get('/', response_model=PaginatedResponse[ChatResponse])
def list_chats(
    service: ChatServiceDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[int] = Query(None),
):
    return service.paginated_list(
        page=page,
        page_size=page_size,
        user_id=user_id,
    )


@router.get('/{chat_id}/messages', response_model=list[MessageResponse])
def list_chat_messages(chat_id: int, service: MessageServiceDep):
    return service.list_by_chat(chat_id)


@router.post('/', response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat(chat: ChatCreate, service: ChatServiceDep):
    return service.create(chat)


@router.delete('/{chat_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: int, service: ChatServiceDep):
    service.delete(chat_id)


@router.patch('/{chat_id}/rename', response_model=ChatResponse)
def update_chat_name(
    chat_id: int,
    chat_rename: ChatRename,
    service: ChatServiceDep,
):
    return service.update_name(chat_id, chat_rename.name)
