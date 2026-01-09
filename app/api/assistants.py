from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import SessionLocal
from app.schemas.assistant import AssistantCreate, AssistantUpdate, AssistantResponse
from app.services.assistant_service import AssistantService

router = APIRouter(prefix="/assistants", tags=["Assistants"])


def get_assistant_service() -> AssistantService:
    return AssistantService(session=SessionLocal())


@router.get("/{assistant_id}", response_model=AssistantResponse)
def get_assistant(
    assistant_id: int,
    service: AssistantService = Depends(get_assistant_service)
):
    assistant = service.get_assistant(assistant_id)
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return assistant


@router.get("/", response_model=list[AssistantResponse])
def list_assistants(
    service: AssistantService = Depends(get_assistant_service)
):
    return service.list_assistants()


@router.post("/", response_model=AssistantResponse, status_code=status.HTTP_201_CREATED)
def create_assistant(
    assistant: AssistantCreate,
    service: AssistantService = Depends(get_assistant_service)
):
    return service.create_assistant(assistant)


@router.put("/{assistant_id}", response_model=AssistantResponse)
def update_assistant(
    assistant_id: int,
    payload: AssistantUpdate,
    service: AssistantService = Depends(get_assistant_service)
):
    assistant = service.get_assistant(assistant_id)
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")

    return service.update_assistant(assistant, payload)


@router.delete("/{assistant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assistant(
    assistant_id: int,
    service: AssistantService = Depends(get_assistant_service)
):
    assistant = service.get_assistant(assistant_id)
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")

    service.delete_assistant(assistant)
