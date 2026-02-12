from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.message import MasssageUpdate, MessageCreate, MessageResponse
from app.services.message_service import MessageService

router = APIRouter(prefix='/messages', tags=['Messages'])


def get_message_service(db: Annotated[Session, Depends(get_db)]) -> MessageService:
    return MessageService(session=db)


MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]


@router.post('/', response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_message(message: MessageCreate, service: MessageServiceDep):
    return service.create_with_response(message)


@router.put('/{message_id}', response_model=MessageResponse)
def update_message(
    message_id: int,
    payload: MasssageUpdate,
    service: MessageServiceDep,
):
    message = service.get_message(message_id)
    if not message:
        raise HTTPException(status_code=404, detail='Message not found')

    return service.update_message(message, payload.content)
