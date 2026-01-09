from sqlalchemy.orm import Session
from uuid import UUID

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    def __init__(self, session: Session):
        self._db = session
    
    def create_user(self, data: UserCreate) -> User:
        user = User(**data.dict())
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def get_user(self, user_id: int) -> User | None:
        return self._db.query(User).filter(User.id == user_id).first()

    def list_users(self):
        return self._db.query(User).order_by(User.created_at.desc()).all()

    def update_user(self, user: User, data: UserUpdate) -> User:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(user, field, value)

        self._db.commit()
        self._db.refresh(user)
        return user

    def delete_user(self, user: User):
        self._db.delete(user)
        self._db.commit()