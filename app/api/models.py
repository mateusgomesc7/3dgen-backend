from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.model import ModelCreate, ModelUpdate, ModelResponse
from app.services.model_service import ModelService

router = APIRouter(prefix="/models", tags=["Models"])


def get_model_service(db: Session = Depends(get_db)) -> ModelService:
    return ModelService(session=db)


@router.get("/{model_id}", response_model=ModelResponse)
def get_model(
    model_id: int,
    service: ModelService = Depends(get_model_service)
):
    model = service.get_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model


@router.get("/", response_model=list[ModelResponse])
def list_models(
    is_active: Optional[bool] = None,
    service: ModelService = Depends(get_model_service)
):
    return service.list_models(is_active=is_active)


@router.post("/", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
def create_model(
    model: ModelCreate,
    service: ModelService = Depends(get_model_service)
):
    return service.create_model(model)


@router.put("/{model_id}", response_model=ModelResponse)
def update_model(
    model_id: int,
    payload: ModelUpdate,
    service: ModelService = Depends(get_model_service)
):
    model = service.get_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    return service.update_model(model, payload)


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_model(
    model_id: int,
    service: ModelService = Depends(get_model_service)
):
    model = service.get_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    service.delete_model(model)
