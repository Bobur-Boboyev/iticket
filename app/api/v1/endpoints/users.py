from typing import Annotated

from fastapi import APIRouter, Depends, Body, Path

from app.core.security import get_user, get_admin
from app.db.session import get_db
from app.models.user import User
from app.services.user_service import UserService
from app.schemas.user import UserResponse, UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=list[UserResponse])
async def users_view(
    admin: Annotated[User, Depends(get_admin)], db: Annotated[User, Depends(get_db)]
):
    user_service = UserService(db)
    users = user_service.get_all_users()

    return users


@router.get("/{id}", response_model=UserResponse)
async def get_user_view(
    id: Annotated[int, Path()],
    user: Annotated[User, Depends(get_user)],
    db: Annotated[User, Depends(get_db)],
):
    user_service = UserService(db)
    user = user_service.get_current_user(id, user)
    return user


@router.patch("/{id}", response_model=UserResponse)
async def update_user_view(
    id: Annotated[int, Path()],
    data: Annotated[UserUpdate, Body()],
    user: Annotated[User, Depends(get_user)],
    db: Annotated[User, Depends(get_db)],
):
    user_service = UserService(db)
    updated_user = user_service.update_user(id, data, user)

    return updated_user
