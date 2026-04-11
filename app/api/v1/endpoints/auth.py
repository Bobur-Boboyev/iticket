from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import get_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    UserRegistration,
    UserLoginResponse,
    UserResponse,
    RefreshRequest,
)
from app.services.user_service import UserService


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", response_model=UserResponse)
async def register_view(
    user_data: Annotated[UserRegistration, Body()],
    db: Annotated[Session, Depends(get_db)],
):
    user_service = UserService(db)
    user = user_service.create_user(user_data)

    return user


@router.post("/login", response_model=UserLoginResponse)
async def login_view(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user_service = UserService(db)
    login_response = user_service.authenticate_user(data)

    return login_response


@router.post("/refresh", response_model=UserLoginResponse)
async def refresh_view(
    data: Annotated[RefreshRequest, Body()], db: Annotated[Session, Depends(get_db)]
):
    user_service = UserService(db)
    refresh_response = user_service.refresh_access_token(data.refresh_token)
    return refresh_response


@router.get("/me", response_model=UserResponse)
async def me_view(user: Annotated[User, Depends(get_user)]):
    return user
