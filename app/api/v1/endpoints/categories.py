from typing import Annotated

from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_admin
from app.models.user import User
from app.schemas.category import CategoryResponse, CreateCategory
from app.services.category_service import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.get("/", response_model=list[CategoryResponse])
async def categories_view(db: Annotated[Session, Depends(get_db)]):
    category_service = CategoryService(db)
    categories = category_service.get_all_categories()

    return categories


@router.post("/", response_model=CategoryResponse)
async def create_category_view(
    data: Annotated[CreateCategory, Body()],
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin)],
):
    category_service = CategoryService(db)
    category = category_service.create_category(name=data.name)

    return category


@router.delete("/{id}", status_code=204)
async def delete_category_view(
    id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin)],
):
    category_service = CategoryService(db)
    category_service.delete_category(id)