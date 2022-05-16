from fastapi import HTTPException
from . import models, schemas

from sqlalchemy.orm import Session
import typing


def get_categories(db: Session) -> list[schemas.Category]:
    return db.query(models.Category).all()

def get_category_by_id(db: Session, id: int) -> models.Category | None:
    return db.query(models.Category).filter(models.Category.id == id).first()

def create_category(db: Session, category: schemas.CategoryBase) -> models.Category:
    db_category = models.Category(title=category.title, color=category.color, points=[])
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_points(db: Session) -> list[models.Point]:
    return db.query(models.Point).all()


def create_point(db: Session, point: schemas.PointCreate) -> models.Point | None:
    db_category = get_category_by_id(db, point.category_id)
    if db_category is None:
        return None
    db_point = models.Point(x=point.x, 
                            y=point.y, 
                            name=point.name, 
                            description=point.description, 
                            rating=0,
                            category_id=db_category.id
                            )
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point


# typing.BinaryIO
def create_photo(db: Session, filename: str, file: typing.BinaryIO, point_id) -> models.Photo:
    with open(f'static/{filename}', 'wb') as f:
        f.write(file.read())
    db_photo = models.Photo(url = f'static/{filename}', point_id=point_id)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo


def plus_rating(db: Session, point_id) -> bool:
    db_point = db.query(models.Point).filter(models.Point.id == point_id).first()
    if db_point is None:
        raise HTTPException(400, f'Point(id={point_id}) is None')
    db_point.rating = db_point.rating + 1
    db.commit()
    return True


def minus_rating(db: Session, point_id) -> bool:
    db_point = db.query(models.Point).filter(models.Point.id == point_id).first()
    if db_point is None:
        raise HTTPException(400, f'Point(id={point_id}) is None')
    db_point.rating = db_point.rating - 1
    db.commit()
    return True
