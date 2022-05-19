from tkinter import OFF
from fastapi import HTTPException
from . import models, schemas

from sqlalchemy.orm import Session
import typing
import hashlib


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


def get_points_by_category_id(db: Session, category_id: int) -> list[models.Point]:
    return db.query(models.Point).filter(models.Point.category_id == category_id).all()


def create_point(db: Session, point: schemas.PointCreate) -> models.Point | None:
    db_category = get_category_by_id(db, point.category_id)
    if db_category is None:
        return None
    db_point = models.Point(x=point.x, 
                            y=point.y, 
                            offset=point.offset,
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
def create_photo(db: Session, filename: str, file: typing.BinaryIO, point_id: int) -> models.Photo:
    with open(f'static/{filename}', 'wb') as f:
        f.write(file.read())
    db_photo = models.Photo(url = f'static/{filename}', point_id=point_id)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo


def plus_rating(db: Session, point_id: int) -> bool:
    db_point = db.query(models.Point).filter(models.Point.id == point_id).first()
    if db_point is None:
        raise HTTPException(400, f'Point(id={point_id}) is None')
    db_point.rating = db_point.rating + 1
    db.commit()
    return True


def minus_rating(db: Session, point_id: int) -> bool:
    db_point = db.query(models.Point).filter(models.Point.id == point_id).first()
    if db_point is None:
        raise HTTPException(400, f'Point(id={point_id}) is None')
    db_point.rating = db_point.rating - 1
    db.commit()
    return True


def get_comments_by_point_id(db: Session, point_id: int):
    return db.query(models.Comment).filter(models.Comment.point_id == point_id).all()


def create_comment_by_point_id(db: Session, point_id: int, comment: schemas.CommentCreate, author: str):
    db_comment = models.Comment(author=author, text=comment.text, point_id=point_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def create_user(db: Session, user: schemas.User) -> models.User:
    db_password = hashlib.sha224(user.password.encode()).hexdigest()
    db_user = models.User(login=user.login, password=db_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user: schemas.User) -> bool:
    return db.query(models.User).filter(models.User.login == user.login).first()


def create_session(db: Session, token: str):
    db_session = models.Sessions(token=token)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return True


def delete_session(db: Session, token: str):
    db_session = db.query(models.Sessions).filter(models.Sessions.token == token).first()
    db.delete(db_session)
    db.commit()
    return True


def get_session(db: Session, token: str):
    return db.query(models.Sessions).filter(models.Sessions.token == token).first()