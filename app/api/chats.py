from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import SessionLocal
from app.schemas.chat import ChatCreate, ChatUpdate, ChatResponse
from app.schemas.message import MessageResponse
from app.services.chat_service import ChatService
from app.services.message_service import MessageService

router = APIRouter(prefix="/chats", tags=["Chats"])


def get_chat_service() -> ChatService:
    return ChatService(session=SessionLocal())

def get_message_service() -> MessageService:
    return MessageService(session=SessionLocal())


@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(
    chat_id: int,
    service: ChatService = Depends(get_chat_service)
):
    chat = service.get(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.get("/", response_model=list[ChatResponse])
def list_chats(
    service: ChatService = Depends(get_chat_service)
):
    return service.list()


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat(
    chat: ChatCreate,
    service: ChatService = Depends(get_chat_service)
):
    return service.create(chat)


@router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(
    chat_id: int,
    payload: ChatUpdate,
    service: ChatService = Depends(get_chat_service)
):
    chat = service.get(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    return service.update(chat, payload)

@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(
    chat_id: int,
    service: ChatService = Depends(get_chat_service)
):
    chat = service.get(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    service.delete(chat)

@router.get("/{chat_id}/messages", response_model=list[MessageResponse])
def list_chat_messages(
    chat_id: int,
    service: MessageService = Depends(get_message_service)
):
    return service.list_by_chat(chat_id)
