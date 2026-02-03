from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.provider import ProviderResponse
from app.schemas.model import ModelResponse
from app.services.provider_service import ProviderService

router = APIRouter(prefix="/providers", tags=["Providers"])


def get_provider_service(db: Session = Depends(get_db)) -> ProviderService:
    return ProviderService(session=db)


@router.get("/{provider_id}", response_model=ProviderResponse)
def get_provider(
    provider_id: int,
    service: ProviderService = Depends(get_provider_service)
):
    provider = service.get_provider(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


@router.get("/", response_model=list[ProviderResponse])
def list_providers(
    is_active: Optional[bool] = None,
    service: ProviderService = Depends(get_provider_service)
):
    return service.list_providers(is_active=is_active)


@router.get("/{provider_id}/models", response_model=list[ModelResponse])
def get_provider_models(
    provider_id: int,
    service: ProviderService = Depends(get_provider_service)
):
    return service.get_provider_models(provider_id=provider_id)


@router.post("/sync/{provider_id}", response_model=str)
def sync_providers(
    provider_id: int,
    service: ProviderService = Depends(get_provider_service)
):
    return service.sync_providers(provider_id=provider_id)