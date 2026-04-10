from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models import User
from app.core.security import (
    generate_token,
    generate_refresh_token,
    verify_access_token,
    verify_refresh_token,
    hash_password,
    verify_password,
)
from app.schemas.user import UserRegistration, UserLoginResponse, UserLogin


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(
        self,
        user_data: UserRegistration,
    ) -> User:
        if self.get_user_by_username(user_data.username):
            raise HTTPException(status_code=400, detail="Username already exists")

        if self.get_user_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already exists")

        hashed_password = hash_password(user_data.password)
        user = User(
            username=user_data.username,
            role=user_data.role,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password_hash=hashed_password,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def authenticate_user(self, data: UserLogin) -> UserLoginResponse | None:
        user = self.get_user_by_username(data.username)

        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        token_data = {"sub": f"{user.id}", "username": user.username}

        access_token = generate_token(token_data)
        refresh_token = generate_refresh_token(token_data)

        return UserLoginResponse(access_token=access_token, refresh_token=refresh_token)
    
    def refresh_access_token(self, refresh_token: str) -> UserLoginResponse:

        payload = verify_refresh_token(refresh_token)

        user_id = payload.get("sub")

        user = self.get_user_by_id(user_id)
    
        if not self.get_user_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        new_access_token = generate_token({"sub": f"{user.id}", "username": user.username})

        return UserLoginResponse(access_token=new_access_token, refresh_token=refresh_token)

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()
