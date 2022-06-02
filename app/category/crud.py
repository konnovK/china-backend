from app.database import model
from app.category import schema

from sqlalchemy.orm import Session


def get_categories(db: Session) -> list[model.Category]:
    return db.query(model.Category).all()


def create_category(db: Session, category: schema.CategoryCreate) -> model.Category:
    db_category = model.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category_points(db: Session, id: int) -> list[model.Point]:
    return db.query(model.Point).filter(model.Point.category_id == id).all()


def get_category_by_id(db: Session, category_id: int) -> model.Category:
    return db.query(model.Category).filter(model.Category.id == category_id).first()
