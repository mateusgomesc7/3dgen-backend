from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import SessionLocal
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import MessageService

router = APIRouter(prefix="/messages", tags=["Messages"])


def get_message_service() -> MessageService:
    return MessageService(session=SessionLocal())


@router.post("/", response_model=list[MessageResponse], status_code=status.HTTP_201_CREATED)
def create_message(
    message: MessageCreate,
    service: MessageService = Depends(get_message_service)
):
    return service.create_with_response(message)
