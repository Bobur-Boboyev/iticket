from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Category


class CategoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_category(self, name: str) -> Category:
        existing = self.db.query(Category).filter(Category.name == name).first()
        if existing:
            raise HTTPException(
                status_code=400, detail="Category with this name already exists"
            )

        category = Category(name=name)

        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category

    def get_all_categories(self) -> list[Category]:
        categories = self.db.query(Category).all()
        return categories
    
    def get_category_by_id(self, id: int) -> Category:
        category = self.db.query(Category).filter(Category.id == id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    
    def delete_category(self, id: int):
        category = self.get_category_by_id(id)
        self.db.delete(category)
        self.db.commit()