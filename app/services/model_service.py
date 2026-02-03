from sqlalchemy.orm import Session

from app.models.model import Model
from app.models.message import Message
from app.schemas.model import ModelCreate, ModelUpdate
from app.exceptions.base import NotFoundException, ConflictException

class ModelService:
    def __init__(self, session: Session):
        self._db = session
    
    def create_model(self, data: ModelCreate) -> Model:
        model = Model(**data.dict())
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return model

    def get_model(self, model_id: int) -> Model | None:
        return self._db.query(Model).filter(Model.id == model_id).first()

    def list_models(self, is_active: bool | None = None) -> list[Model]:
        query = self._db.query(Model).order_by(Model.id.desc())
        if is_active is not None:
            query = query.filter(Model.is_active == is_active)
        return query.all()

    def update_model(self, model: Model, data: ModelUpdate) -> Model:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(model, field, value)

        self._db.commit()
        self._db.refresh(model)
        return model

    def delete_model(self, model_id: int) -> None:
        model = self.get_model(model_id)

        if not model:
            raise NotFoundException(f"Model with ID {model_id} not found.")

        has_messages = self._db.query(Message).filter(Message.model_id == model_id).first()
        if has_messages:
            raise ConflictException("Cannot delete model: it has linked messages.")

        self._db.delete(model)
        self._db.commit()
    