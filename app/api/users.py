from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix='/users', tags=['Users'])


def get_user_service(db: Annotated[Session, Depends(get_db)]) -> UserService:
    return UserService(session=db)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: int, service: UserServiceDep):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.get('/', response_model=list[UserResponse])
def list_users(service: UserServiceDep):
    return service.list_users()


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, service: UserServiceDep):
    return service.create_user(user)


@router.put('/{user_id}', response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, service: UserServiceDep):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return service.update_user(user, payload)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserServiceDep):
    service.delete_user(user_id)
