from . import models, schemas

from sqlalchemy.orm import Session


def get_categories(db: Session) -> list[models.Category]:
    return db.query(models.Category).all()

def get_category_by_title(db: Session, title: str):
    return db.query(models.Category).filter(models.Category.title == title).first()

def create_category(db: Session, category: schemas.CategoryBase) -> models.Category:
    db_category = models.Category(title=category.title, color=category.color, points=[])
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_points(db: Session) -> list[models.Point]:
    return db.query(models.Point).all()


def create_point(db: Session, point: schemas.PointBase) -> models.Point:
    db_category = get_category_by_title(db, point.category)
    db_point = models.Point(coord_x=point.x, 
                            coord_y=point.y, 
                            name=point.name, 
                            description=point.description, 
                            rating=point.rating,
                            category=db_category 
                            )
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point
