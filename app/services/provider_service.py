from datetime import datetime
from http.client import HTTPException
from sqlalchemy.orm import Session

from app.models.model import Model
from app.models.provider import Provider
from app.services.assistants.factory import get_assistant 

class ProviderService:
    def __init__(self, session: Session):
        self._db = session


    def get_provider(self, provider_id: int) -> Provider | None:
        return self._db.query(Provider).filter(Provider.id == provider_id).first()


    def list_providers(self, is_active: bool | None = None) -> list[Provider]:
        query = self._db.query(Provider).order_by(Provider.id.desc())
        if is_active is not None:
            query = query.filter(Provider.is_active == is_active)
        return query.all()
    

    def get_provider_models(self, provider_id: int) -> list[Model]:
        return self._db.query(Model).filter(Model.provider_id == provider_id).all()

    
    def sync_providers(self, provider_id: int) -> str:
        provider = self.get_provider(provider_id)
        if not provider:
            raise HTTPException(404, f"Provider with ID {provider_id} not found.")

        assistant_ai = get_assistant(provider.name)
        models = assistant_ai.list_models()
        model_names = {m["name"] for m in models}

        all_models = self._db.query(Model).filter(Model.provider_id == provider.id).all()
        existing_models_dict = {a.name: a for a in all_models}

        for name, model in existing_models_dict.items():
            if name in model_names:
                model.is_active = True
                model.last_checked_at = datetime.now()
            else:
                model.is_active = False
                model.last_checked_at = datetime.now()
        new_count = 0
        for model_name in model_names:
            if model_name not in existing_models_dict:
                new_model = Model(
                    name=model_name,
                    provider_id=provider.id,
                    is_active=True,
                    last_checked_at=datetime.now()
                )
                self._db.add(new_model)
                new_count += 1

        self._db.commit()
        return f"Synchronization complete. {new_count} new models added."
    